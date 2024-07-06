import os

from PySide6.QtCore import QRunnable, QObject, Signal


class DirectorySignals(QObject):
    finished = Signal()
    result = Signal(float)


class DirectorySizeWorker(QRunnable):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.signals = DirectorySignals()

    def run(self):
        total_size = 0.0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        self.signals.result.emit(total_size)
        self.signals.finished.emit()