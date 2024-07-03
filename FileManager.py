import os
import shutil
import sys

from PySide6.QtGui import QIcon, QAction, QStandardItem, QCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QHeaderView, QDialog, QMenu
from PySide6.QtCore import QCoreApplication, QMetaObject, Qt, QLocale, QTranslator, QSize, QPersistentModelIndex
from matplotlib import pyplot as plt

from ui.ui_FileManager import Ui_FileManager

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ui.ui_SettingsDialog import Ui_SettingsDialog

PATH_ROOT = os.path.dirname(os.path.abspath(__file__))


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)


class FileManager(QMainWindow, Ui_FileManager):
    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent)
        self.nav_index = 0
        self.setupUi(self)
        self.connect_actions()
        self.history_nav = []
        # Set the application locale to French
        self.translator = QTranslator()
        if self.translator.load("qt_fr.qm"):
            QCoreApplication.installTranslator(self.translator)
        QLocale.setDefault(QLocale(QLocale.French, QLocale.France))
        self.init_toolbar()
        # File System Model
        self.fileSystemModel = QFileSystemModel(self)
        self.fileSystemModel.setRootPath("")

        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(self.fileSystemModel.index(""))
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)

        self.listView.setModel(self.fileSystemModel)
        self.listView.setRootIndex(self.fileSystemModel.index(""))

        self.canvas = FigureCanvas(plt.Figure())
        self.verticalLayout_4.addWidget(self.canvas)
        self.locale = QLocale(QLocale.Language.French)
        self.treeView.setStyleSheet("""
                    QTreeView::item:hover {
                               background-color: dodgerblue;
                               color: white;
                           } 
                    QTreeView::item:selected {
                       background-color: royalblue;
                       color: white;
                   }
               """)
        self.listView.setStyleSheet("""
                           QListView::item:hover {
                               background-color: dodgerblue;
                               color: white;
                           }
                           QListView::item:selected {
                               background-color: royalblue;
                               color: white;
                           }
                           
                       """)

    def init_toolbar(self):
        self.toolBar.setIconSize(QSize(15, 15))
        new_folder = QAction(QIcon(f"{PATH_ROOT}/toolbar/add-folder.png"), "", self)
        cut = QAction(QIcon(f"{PATH_ROOT}/toolbar/cut.png"), "", self)
        copy = QAction(QIcon(f"{PATH_ROOT}/toolbar/copy.png"), "", self)
        config = QAction(QIcon(f"{PATH_ROOT}/toolbar/settings.png"), "", self)
        parent_dir = QAction(QIcon(f"{PATH_ROOT}/toolbar/up.png"), "", self)
        parent_dir.triggered.connect(self.go_to_parent_directory)
        config.triggered.connect(self.open_settings)
        self.toolBar.addAction(new_folder)
        self.toolBar.addAction(cut)
        self.toolBar.addAction(copy)
        self.toolBar.addAction(config)
        self.toolBar.addAction(parent_dir)

    def connect_actions(self):
        self.actionNouveau.triggered.connect(self.new_file)
        self.actionCopier.triggered.connect(self.copy_file)
        self.actionCouper.triggered.connect(self.cut_file)
        self.actionColler.triggered.connect(self.paste_file)
        self.actionSauvegarder.triggered.connect(self.save_file)
        self.actionRenommer.triggered.connect(self.rename_file)
        self.treeView.clicked.connect(self.on_treeView_clicked)
        self.listView.doubleClicked.connect(self.update_lists)
        self.btn_prev.clicked.connect(lambda: self.navigate("prev"))
        self.btn_next.clicked.connect(lambda: self.navigate("next"))
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.open_context_menu)
        self.nav_index = 0

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.setWindowTitle("Paramètres")
        if dialog.exec() == QDialog.Accepted:
            print("Paramètres acceptés")
        else:
            print("Paramètres rejetés")

    def navigate(self, direction):
        if direction == "prev":
            self.nav_index -= 1
            if self.nav_index < 0:
                self.nav_index = len(self.history_nav) - 1
        else:
            self.nav_index += 1
            if self.nav_index >= len(self.history_nav):
                self.nav_index = len(self.history_nav) - 1

        path = self.history_nav[self.nav_index]
        self.listView.setRootIndex(self.fileSystemModel.index(path))
        self.textBrowser.setText(path)

    def new_file(self):
        # Implémenter la fonctionnalité pour créer un nouveau fichier
        print("Nouveau fichier créé")

    def copy_file(self):
        # Implémenter la fonctionnalité pour copier un fichier
        print("Fichier copié")

    def cut_file(self):
        # Implémenter la fonctionnalité pour couper un fichier
        print("Fichier coupé")

    def paste_file(self):
        # Implémenter la fonctionnalité pour coller un fichier
        print("Fichier collé")

    def save_file(self):
        # Implémenter la fonctionnalité pour sauvegarder un fichier
        print("Fichier sauvegardé")

    def rename_file(self):
        # Implémenter la fonctionnalité pour renommer un fichier
        print("Fichier renommé")

    def delete_file(self):
        # Implémenter la fonctionnalité pour renommer un fichier
        print("Fichier supprimé")

    def execute_command(self):
        print("Commande")

    def on_treeView_clicked(self, index):
        self.infos(index)

    def infos(self, index):
        self.listView.setRootIndex(index)
        self.listView.setRootIndex(index)
        model = self.fileSystemModel
        parent_index = model.parent(index)

        file_path = self.fileSystemModel.filePath(index)
        file_info = self.fileSystemModel.fileInfo(index)

        self.textBrowser.setText(file_path)
        self.history_nav.insert(self.nav_index, file_path)

        self.lbl_preview.setVisible(True if file_info.exists() else False)

        file_name = file_info.fileName()
        if file_name == "" and not file_info.isFile():
            file_name = "Lecteur " + file_path[:-2]
            self.lbl_nom.setText(f"{file_name}")
        else:
            self.lbl_nom.setText(f"Nom: {file_name}")

        self.lbl_chemin.setText(f"Chemin: {file_path}")

        last_modified_date = self.locale.toString(file_info.lastModified(), QLocale.FormatType.LongFormat)
        self.lbl_date.setText(f"Date de modification: {last_modified_date}")

        self.lbl_type.setText(f"Type: {file_info.suffix() if file_info.isFile() else 'Dossier'}")

        if file_info.isDir():
            if os.path.ismount(file_path):
                total_size, free_space = self.get_disk_usage(file_path)
                directory_size = total_size - free_space
                percentage = (directory_size / total_size) * 100 if total_size > 0 else 0
                self.draw_pie_chart(total_size, free_space)
                total_size = self.get_size(total_size)
                free_space = self.get_size(free_space)
                self.lbl_taille.setText(f"Taille totale / dispo : {total_size} / {free_space} ({percentage:.2f}%)")
            else:
                directory_size = self.get_directory_size(file_path)
                if directory_size > 0:
                    root_size, _ = self.get_disk_usage(os.path.abspath(os.sep))
                    percentage = (directory_size / root_size) * 100 if root_size > 0 else 0
                    self.draw_pie_chart(root_size, directory_size)
                    directory_size = self.get_size(directory_size)
                    self.lbl_taille.setText(f"Taille du répertoire : {directory_size} ({percentage:.2f}%)")
                else:
                    self.lbl_taille.setText(f"Taille du répertoire : vide ")

        else:
            file_size = file_info.size()
            total_size, free_space = self.get_disk_usage(os.path.abspath(os.sep))
            percentage = (file_size / total_size) * 100 if total_size > 0 else 0
            file_size = self.get_size(file_size)
            self.lbl_taille.setText(f"Taille du fichier : {file_size} ({percentage:.2f}%)")

    def get_directory_size(self, directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size

    def get_disk_usage(self, path):
        usage = shutil.disk_usage(path)
        return usage.total, usage.free

    def get_size(self, size, decimal_places=2):
        for unit in ['Octets', 'Ko', 'Mo', 'Go', 'To', 'Po']:
            if size < 1024.0:
                return f"{size:.{decimal_places}f} {unit}"
            size /= 1024.0

    def draw_pie_chart(self, total_size, free_space):
        used_space = total_size - free_space
        sizes = [used_space, free_space]
        labels = ['Espace utilisé', 'Espace libre']
        colors = ['#ff9999', '#66b3ff']

        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=70, shadow=True, radius=0.8,
               wedgeprops=dict(width=0.5, edgecolor='black'))
        ax.axis('equal')
        self.canvas.draw()

    def update_lists(self, index):
        self.nav_index = len(self.history_nav) - 1
        self.infos(index)

    def go_to_parent_directory(self):
        # current_index = self.treeView.currentIndex()
        current_index = self.listView.currentIndex()
        if not current_index.isValid():
            return

        parent_index = self.fileSystemModel.parent(current_index)
        if parent_index.isValid():
            # self.treeView.setRootIndex(parent_index)
            self.update_lists(parent_index)

    def open_context_menu(self, position):
        indexes = self.treeView.selectedIndexes()
        if not indexes:
            return

        menu = QMenu()
        cut_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/cut.png"), "Couper", self)
        copy_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/copy.png"), "Copier", self)
        rename_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/rename.png"), "Renommer", self)
        delete_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/remove-folder.png"), "Supprimer", self)
        command_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/running.png"), "Exécuter commande", self)

        cut_action.triggered.connect(self.cut_file)
        copy_action.triggered.connect(self.copy_file)
        rename_action.triggered.connect(self.rename_file)
        delete_action.triggered.connect(self.delete_file)
        command_action.triggered.connect(self.execute_command)

        menu.addAction(cut_action)
        menu.addAction(copy_action)
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        menu.addAction(command_action)

        menu.exec(QCursor.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the application locale to French
    translator = QTranslator()
    if translator.load("qt_fr.qm"):
        app.installTranslator(translator)
    QLocale.setDefault(QLocale(QLocale.French, QLocale.France))

    mainWindow = FileManager()
    mainWindow.show()
    sys.exit(app.exec())
