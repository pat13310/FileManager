from PySide6.QtWidgets import QDialog

from ui.ui_SettingsDialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)
