import os
import shutil
import json
from pathlib import Path
from PySide6.QtCore import QRunnable, Signal, QObject, QThreadPool
from Plugin import PluginManager


class CleanerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    message = Signal(str)
    progress = Signal(int)
    cancelled = Signal()


class Cleaner(QRunnable):
    def __init__(self, config_file_path):
        super(Cleaner, self).__init__()
        self.signals = CleanerSignals()
        self.cancel_requested = False
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        # Charger la configuration depuis le fichier JSON
        self.config = self.load_config(config_file_path)
        self.paths_to_clean = self.prepare_paths_to_clean()
        self._is_running = False

    def load_config(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            self.signals.error.emit(f"Le fichier de configuration '{file_path}' n'a pas été trouvé.")
            return None
        except json.JSONDecodeError as e:
            self.signals.error.emit(f"Erreur de décodage JSON : {e}")
            return None

    def prepare_paths_to_clean(self):
        paths_to_clean = []
        for category, category_details in self.config['Configurations'].items():
            # Pas de vérification pour 'enabled' au niveau de la catégorie
            for path_name, path_info in category_details['options'].items():
                if path_info.get('enabled', False):  # Vérifie si chaque chemin est activé
                    path_obj = Path(path_info['path'].replace("<Username>", os.getenv("USERNAME")))
                    if path_obj.exists():
                        paths_to_clean.append(path_obj)
        return paths_to_clean

    def run(self):
        self._is_running = True
        try:
            self.plugin_manager.run_plugins("before_cleanup")
            for path in self.paths_to_clean:
                if self.cancel_requested:
                    self._is_running = False
                    self.signals.cancelled.emit()
                    return
                self.clean_directory(path)
            self.plugin_manager.run_plugins("after_cleanup")
            if not self.cancel_requested:
                self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(f"Erreur : {str(e)}")
        finally:
            self._is_running = False

    def clean_directory(self, directory):
        total_files = sum(1 for _ in directory.rglob('*') if _.is_file())
        processed_files = 0
        for item in directory.rglob('*'):
            if self.cancel_requested:
                self._is_running = False
                break
            try:
                if item.is_file():
                    self.secure_erase(item)
                elif item.is_dir():
                    shutil.rmtree(item)
                processed_files += 1
                self.update_progress(processed_files, total_files)
            except Exception:
                self.signals.error.emit(f"Impossible de supprimer de {item}")

    def secure_erase(self, file_path):
        try:
            # with open(file_path, "ba+") as file:
            #     length = file.tell()
            #     for _ in range(3):
            #         file.seek(0)
            #         file.write(os.urandom(length))
            os.remove(file_path)
        except Exception as e:
            print(f"Erreur lors du nettoyage : {e}")
            self.signals.error.emit(f"Impossible de supprimer de {file_path}")

    def update_progress(self, processed, total):
        if total > 0:
            progress_percent = int((processed / total) * 100)
            self.signals.progress.emit(progress_percent)

    def stop(self):
        self.cancel_requested = True

    def is_running(self):
        return self._is_running
