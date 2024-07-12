import os

from PySide6.QtCore import QRunnable, Slot, Signal, QObject


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(str)
    deleted = Signal()
    permission_admin = Signal()


class DeleteFilesWorker(QRunnable):
    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.delete_files(self.file_paths)
            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))

    def delete_files(self, file_paths):
        for file_path in file_paths:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                self.signals.deleted.emit()
            except PermissionError as e:
                print(f"PermissionError: {e}")
                self.signals.permission_admin.emit()
            except FileNotFoundError as e:
                print(f"FileNotFoundError: {e}")
                self.signals.error.emit(str(e))
