from PySide6.QtCore import Qt, QThreadPool, QTimer, QRect
from PySide6.QtGui import QColor, QPainterPath, QPainter, QBrush, QPen
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QGraphicsDropShadowEffect,
)

from Cleaner.CleanOptionsDialog import CleanOptionsDialog
from Cleaner.Cleaner import Cleaner
from ui.ui_ProgressDlg import Ui_progressDlg


class CleanDialog(QDialog, Ui_progressDlg):
    def __init__(self, config_file_path, parent=None):
        super(CleanDialog, self).__init__(parent)
        self.buttonBox = QDialogButtonBox(self)
        self.okButton = QPushButton("Démarrer")
        self.cancelButton = QPushButton("Fermer")
        self.optionsButton = QPushButton("Options")
        self.parent = parent
        self.config_file_path = config_file_path
        self.setupUi(self)
        self.apply_stylesheet()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.add_shadow_effect()
        self.init_buttons()
        self.center_in_parent()
        self.thread_pool = QThreadPool()  # Initialiser le pool de threads
        self.cleaner = None
        self.progressBar.setValue(0)
        self.lblPercent.setText("")
        self.config_file_path = config_file_path
        self.lblMessage.setText("  Prêt")

    def connect_cleaner_signals(self):
        """Connecter les signaux du cleaner aux slots correspondants."""
        self.cleaner.signals.progress.connect(self.set_progress)
        self.cleaner.signals.message.connect(self.set_message)
        self.cleaner.signals.finished.connect(self.cleaning_finished)
        self.cleaner.signals.error.connect(self.cleaning_error)

    def init_buttons(self):
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.addButton(self.okButton, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancelButton, QDialogButtonBox.RejectRole)
        self.buttonBox.addButton(self.optionsButton, QDialogButtonBox.HelpRole)
        self.verticalLayout.addWidget(self.buttonBox)

        self.okButton.clicked.connect(
            self.start_cleaning
        )  # Connecter le bouton à start_cleaning
        self.cancelButton.clicked.connect(
            self.stop_cleaning
        )  # Connecter pour arrêter le nettoyage
        self.optionsButton.clicked.connect(self.show_options_dialog)

    def show_options_dialog(self):
        options_dialog = CleanOptionsDialog(self.config_file_path)
        options_dialog.exec()

    def add_shadow_effect(self):
        # Créer un effet d'ombre
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)  # Rayon du flou de l'ombre
        shadow.setXOffset(5)  # Décalage horizontal de l'ombre
        shadow.setYOffset(5)  # Décalage vertical de l'ombre
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        # Dessine un fond avec des coins arrondis
        path = QPainterPath()
        path.addRoundedRect(QRect(0, 0, self.width(), self.height()), 10, 10)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(path, QBrush(QColor(240, 240, 240)))  # Couleur de fond
        pen = QPen(QColor(200, 200, 200), 1)  # Couleur et épaisseur du bord
        painter.setPen(pen)
        painter.drawPath(path)

    def apply_stylesheet(self):
        # Définir la feuille de style pour l'ensemble de la boîte de dialogue
        self.setStyleSheet("""
           QDialog {
               background-color: #f0f0f0;
               border: 1px solid #c0c0c0;
               border-radius: 10px;
           }
           QPushButton {
               background-color: #2fafe7;
               color: white;
               border: none;
               padding: 3px;
               border-radius: 5px;
               min-height: 20px;
               min-width: 80px;
           }
           QPushButton:hover {
               background-color: #1e88e5;
           }
           QPushButton:pressed {
               background-color: #1565c0;
           }
           QProgressBar {
               border: 1px solid #c0c0c0;
               border-radius: 5px;
               text-align: center;
           }
           QProgressBar::chunk {
               background-color: #2fafe7;
               width: 20px; /* Largeur des blocs de la barre de progression */
           }
           QLabel {
               color: #333;
           }
           """)

    def center_in_parent(self):
        """Centre la boîte de dialogue par rapport à sa fenêtre parente ou au centre de l'écran si aucun parent."""
        if self.parent:
            parent_geometry = self.parent.frameGeometry()
            self_geometry = self.frameGeometry()
            center_point = parent_geometry.center()
            self_geometry.moveCenter(center_point)
            self.move(self_geometry.topLeft())
        else:
            # Si aucun parent n'est spécifié, centre sur l'écran
            screen_geometry = self.screen().geometry()
            self_geometry = self.frameGeometry()
            center_point = screen_geometry.center()
            self_geometry.moveCenter(center_point)
            self.move(self_geometry.topLeft())

    def start_cleaning(self):
        if (
            not self.cleaner or not self.cleaner.is_running()
        ):  # Vérifier si Cleaner n'est pas déjà en cours d'exécution
            self.cleaner = Cleaner(
                self.config_file_path
            )  # Créer une nouvelle instance de Cleaner
            self.connect_cleaner_signals()  # Connecter les signaux de la nouvelle instance
            self.thread_pool.start(
                self.cleaner
            )  # Démarrer Cleaner via le pool de threads

    def stop_cleaning(self):
        if (
            self.cleaner and self.cleaner.is_running()
        ):  # Vérifier si Cleaner est en cours d'exécution
            self.cleaner.request_cancel()  # Demander l'arrêt du nettoyage
        QTimer.singleShot(500, self.reject)

    def set_progress(self, value):
        self.progressBar.setValue(value)
        self.lblPercent.setText(str(value) + " %")

    def set_message(self, message):
        self.lblMessage.setText(message)

    def cleaning_finished(self):
        self.lbl_action.setText("Nettoyage terminé avec succès.")
        self.lblMessage.setText("")
        self.progressBar.setValue(0)
        self.lblPercent.setText("")

        QTimer.singleShot(3000, self.reject)

    def cleaning_error(self, error_message):
        self.lblMessage.setText(f"Erreur: {error_message}")


if __name__ == "__main__":
    # Utilisation de CleanDialog avec une instance de Cleaner
    config_file_path = (
        "../scanner.json"  # Remplacez par le chemin de votre fichier de configuration
    )
    dialog = CleanDialog(config_file_path)
    dialog.show()
