import mimetypes
import os
import time
from os import stat, path
import pathlib

from PySide6.QtCore import QRunnable, QObject, Signal, QMutex, QMutexLocker


class DirectorySignals(QObject):
    finished = Signal()
    result = Signal(float)
    file_type_detected = Signal(str, str)


class DirectorySizeWorker(QRunnable):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.signals = DirectorySignals()
        self._stop_requested = False
        self._mutex = QMutex()

    def run(self):
        total_size = 0.0
        for dirpath, dirnames, filenames in os.walk(self.path):
            with QMutexLocker(self._mutex):
                if self._stop_requested:
                    break
            for filename in filenames:
                with QMutexLocker(self._mutex):
                    if self._stop_requested:
                        break
                file_path = path.join(dirpath, filename)
                total_size += path.getsize(file_path)
                #mime_type, _ = mimetypes.guess_type(url=file_path)
                #self.signals.file_type_detected.emit(mime_type, file_path)
            else:
                continue
            break

        self.signals.result.emit(total_size)
        self.signals.finished.emit()

    def stop(self):
        with QMutexLocker(self._mutex):
            self._stop_requested = True


    class FileInfos:
        def __init__(self):
            pass

        def get_file_attributes(file_path):
            """
            Récupère les attributs complets d'un fichier ou d'un dossier.

            :param file_path: Chemin du fichier ou du dossier.
            :return: Dictionnaire contenant les attributs du fichier ou du dossier.
            """
            file_path = pathlib.Path(file_path)

            if not file_path.exists():
                print(f"Le chemin {file_path} n'existe pas.")
                return None

            attributes = {}

            # Informations de base
            attributes['Path'] = str(file_path)
            attributes['Size'] = file_path.stat().st_size
            attributes['Last Modified'] = time.ctime(file_path.stat().st_mtime)
            attributes['Last Accessed'] = time.ctime(file_path.stat().st_atime)
            attributes['Date Creation'] = time.ctime(file_path.stat().st_ctime)

            # Permissions
            mode = file_path.stat().st_mode
            attributes['Mode'] = mode
            attributes['Read'] = os.access(file_path, os.R_OK)
            attributes['Write'] = os.access(file_path, os.W_OK)
            attributes['Executable'] = os.access(file_path, os.X_OK)

            # Type de fichier
            if os.stat.S_ISDIR(mode):
                attributes['Type'] = 'Dossier'
            elif stat.S_ISREG(mode):
                attributes['Type'] = 'Fichier'
            elif stat.S_ISLNK(mode):
                attributes['Type'] = 'Raccourci'
            elif stat.S_ISCHR(mode):
                attributes['Type'] = 'Character Device'
            elif stat.S_ISBLK(mode):
                attributes['Type'] = 'Block Device'
            elif stat.S_ISFIFO(mode):
                attributes['Type'] = 'FIFO'
            elif stat.S_ISSOCK(mode):
                attributes['Type'] = 'Socket'
            else:
                attributes['Type'] = 'Inconnu'

            # Attributs supplémentaires sous Windows
            if os.name == 'nt':
                try:
                    import win32api
                    import win32con
                    file_attrs = win32api.GetFileAttributes(str(file_path))
                    attributes['Hidden'] = bool(file_attrs & win32con.FILE_ATTRIBUTE_HIDDEN)
                    attributes['System'] = bool(file_attrs & win32con.FILE_ATTRIBUTE_SYSTEM)
                    attributes['Archive'] = bool(file_attrs & win32con.FILE_ATTRIBUTE_ARCHIVE)
                    attributes['Temporary'] = bool(file_attrs & win32con.FILE_ATTRIBUTE_TEMPORARY)
                except ImportError:
                    print("Module pywin32 non installé, impossible de récupérer les attributs Windows spécifiques.")

            return attributes
