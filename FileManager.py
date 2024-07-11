import ctypes
import mimetypes
import os
import shutil
import subprocess
import sys

from PySide6.QtCore import QCoreApplication, Qt, QLocale, QTranslator, QSize, QThreadPool
from PySide6.QtGui import QIcon, QAction, QCursor, QGuiApplication
from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QDialog, QMenu, QMessageBox, QInputDialog, \
    QWidget, QTreeView, QListView
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from Cleaner.CleanDialog import CleanDialog
from SettingsDialog import SettingsDialog
from Utils.DirectorySizeWorker import DirectorySizeWorker
from Utils.FileUtils import FileUtils
from ui.ui_FileManager import Ui_FileManager

PATH_ROOT = os.path.dirname(os.path.abspath(__file__))


class FileManager(QMainWindow, Ui_FileManager):
    def __init__(self, parent=None):
        super(FileManager, self).__init__(parent)

        self.setupUi(self)
        if len(sys.argv) > 1 and sys.argv[1] == "--admin":
            self.setWindowTitle("Gestionnaire FileManager - Mode Administrateur")
        else:
            self.setWindowTitle("Gestionnaire FileManager")

        print(sys.argv)
        self.worker = None
        self.mime_type = None
        self.nav_index = 0
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
        self.thread_pool = QThreadPool()
        self.cleanDlg = CleanDialog("scanner.json")
        self.center_on_screen()
        self.index_selected = None

        # self.lbl_preview.setWordWrap(True)
        self.scrollArea.setFixedHeight(400)
        # self.scrollAreaContents.setFixedHeight(self.scrollArea.height())
        # self.scrollAreaContents.setMaximumWidth(self.panel_preview.width())
        # self.lbl_preview.setMinimumWidth(self.panel_preview.width())
        # self.lbl_preview.setMaximumWidth(self.panel_preview.width())
        # self.scrollArea.setWidgetResizable(True)

    def init_toolbar(self):
        self.toolBar.setIconSize(QSize(15, 15))
        home = QAction(QIcon(f"{PATH_ROOT}/toolbar/home.png"), "", self)
        cut = QAction(QIcon(f"{PATH_ROOT}/toolbar/cut.png"), "", self)
        copy = QAction(QIcon(f"{PATH_ROOT}/toolbar/copy.png"), "", self)
        config = QAction(QIcon(f"{PATH_ROOT}/toolbar/settings.png"), "", self)
        parent_dir = QAction(QIcon(f"{PATH_ROOT}/toolbar/up.png"), "", self)
        clean = QAction(QIcon(f"{PATH_ROOT}/toolbar/clean.png"), "", self)
        # parent_dir.triggered.connect(self.go_to_parent_directory)
        clean.triggered.connect(self.clean_dir)
        config.triggered.connect(self.open_settings)
        clean.triggered.connect(self.open_clean)
        home.triggered.connect(self.home_dir)
        self.toolBar.addAction(home)
        self.toolBar.addAction(cut)
        self.toolBar.addAction(copy)
        spacer = QWidget()
        self.toolBar.addSeparator()
        spacer.setFixedSize(8, 15)
        self.toolBar.addWidget(spacer)
        self.toolBar.addAction(clean)
        spacer2 = QWidget()
        spacer2.setFixedSize(8, 15)
        self.toolBar.addWidget(spacer2)
        self.toolBar.addAction(config)

    def connect_actions(self):
        self.actionNouveau.triggered.connect(self.new_file)
        self.actionCopier.triggered.connect(self.copy_file)
        self.actionCouper.triggered.connect(self.cut_file)
        self.actionColler.triggered.connect(self.paste_file)
        self.actionSauvegarder.triggered.connect(self.save_file)
        self.actionRenommer.triggered.connect(self.rename_file)
        """  ListView et Treeview """
        self.treeView.clicked.connect(self.on_treeView_clicked)
        self.listView.clicked.connect(self.on_listView_clicked)
        self.listView.doubleClicked.connect(self.update_lists)
        self.btn_prev.clicked.connect(lambda: self.navigate("prev"))
        self.btn_next.clicked.connect(lambda: self.navigate("next"))
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.open_context_menu)
        self.listView.customContextMenuRequested.connect(self.open_context_menu)
        self.nav_index = 0

    def home_dir(self):
        self.listView.setRootIndex(self.fileSystemModel.index(""))
        index = self.listView.currentIndex()
        self.infos(index)

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.setWindowTitle("Paramètres")
        if dialog.exec() == QDialog.Accepted:
            print("Paramètres acceptés")
        else:
            print("Paramètres rejetés")

    def open_clean(self):
        self.cleanDlg.setWindowTitle("Nettoyage")
        if self.cleanDlg.exec() == QDialog.Accepted:
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

    def clean_dir(self):
        pass

    def new_file(self):
        if not self.index_selected.isValid():
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un emplacement valide.")
            return

        current_path = self.fileSystemModel.filePath(self.index_selected)

        # Vérifier si le chemin actuel est un dossier
        if not os.path.isdir(current_path):
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un dossier pour créer un nouvel élément.")
            return

        # Boîte de dialogue pour choisir le type d'élément à créer
        item_type, ok = QInputDialog.getItem(self, "Créer un nouvel élément", "Type d'élément:", ["Dossier", "Fichier"],
                                             0, False)
        if ok and item_type:
            item_name, ok = QInputDialog.getText(self, f"Nouveau {item_type.lower()}",
                                                 f"Nom du nouveau {item_type.lower()}:")
            if ok and item_name:
                item_path = os.path.join(current_path, item_name)
                try:
                    if item_type == "Dossier":
                        os.makedirs(item_path)
                        print(f"Nouveau dossier créé : {item_path}")
                    elif item_type == "Fichier":
                        with open(item_path, 'w') as f:
                            f.write('')
                        print(f"Nouveau fichier créé : {item_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Impossible de créer le {item_type.lower()} : {e}")

    def copy_file(self):
        if not self.index_selected.isValid():
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un emplacement valide.")
            return

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
        if not self.index_selected.isValid():
            return
        old_name = self.fileSystemModel.fileName(self.index_selected)
        new_name, ok = QInputDialog.getText(self, "Renommer", "Nouveau nom:", text=old_name)
        if ok and new_name:
            old_path = self.fileSystemModel.filePath(self.index_selected)
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            os.rename(old_path, new_path)
            self.lbl_chemin.setText(new_path)

    def delete_file(self):

        if not self.index_selected.isValid():
            return
        file_path = self.fileSystemModel.filePath(self.index_selected)
        reply = QMessageBox.question(self, "Supprimer", f"Voulez-vous vraiment supprimer {file_path} ?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Dossier supprimé : {file_path}")
                else:
                    os.chmod(file_path, 0o777)  # Assurez-vous que le fichier n'est pas en lecture seule
                    os.unlink(file_path)
                    # Utilisez subprocess pour supprimer un fichier avec des privilèges élevés sous Windows
                    # command = f'del /F /Q "{file_path}"'
                    # result = subprocess.run(['cmd', '/c', command], capture_output=True, text=True, shell=True)
                    # if result.returncode != 0:
                    #     raise PermissionError(result.stderr)
                    """ on se positionne sur l'index parent s'il existe"""
                    parent_index = self.index_selected.parentIndex()
                    if parent_index is not None:
                        self.listView.setRootIndex(parent_index)
                        self.index_selected = parent_index

                    print(f"Fichier supprimé : {file_path}")

            except PermissionError as perm:
                self.show_admin_dialog(file_path)

                print(f"Permission refusée : {file_path}")
            except OSError as e:
                print(f"Erreur lors de la suppression de {file_path} : {e}")

    def execute_command(self):
        index = self.treeView.currentIndex()
        if not index.isValid():
            return
        file_path = self.fileSystemModel.filePath(index)
        if os.path.isdir(file_path):
            subprocess.Popen([r'C:\Windows\System32\cmd.exe'], cwd=file_path,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            dir_path = os.path.dirname(file_path)
            subprocess.Popen([r'C:\Windows\System32\cmd.exe'], cwd=dir_path,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)

    def on_listView_clicked(self, index):
        self.index_selected = index
        self.infos(index)

    def on_treeView_clicked(self, index):
        self.index_selected = index
        self.listView.setRootIndex(index)
        self.infos(index)

    def show_admin_dialog(self, file):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Vous devez disposer des droits d'administrateur pour supprimer cet élément.")
        msg.setWindowTitle("Accès refusé")
        msg.setStandardButtons(QMessageBox.Ignore | QMessageBox.Cancel | QMessageBox.Ok)

        button_continue = msg.button(QMessageBox.Ok)
        button_continue.setText("Continuer")
        button_ignore = msg.button(QMessageBox.Ignore)
        button_ignore.setText("Ignorer")
        button_cancel = msg.button(QMessageBox.Cancel)
        button_cancel.setText("Annuler")

        result = msg.exec()

        if result == QMessageBox.Ok:
            self.request_admin_rights(file)
        elif result == QMessageBox.Ignore:
            pass  # L'utilisateur a choisi d'ignorer l'action
        elif result == QMessageBox.Cancel:
            self.on_error("Action annulée par l'utilisateur")

    def request_admin_rights(self, file):
        # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable,
        #                                     " ".join([sys.executable] + sys.argv + ["--admin"]), None, 1)
        # QMessageBox.information(self, "Admin Rights Required", "Restarting as admin.")
        params = " ".join(['"' + arg + '"' for arg in sys.argv] + ["--admin"])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()  # Fermez l'application après avoir demandé des droits admin

    def infos(self, index):

        model = self.fileSystemModel
        parent_index = model.parent(index)
        self.canvas.figure.clear()
        file_path = self.fileSystemModel.filePath(index)
        file_info = self.fileSystemModel.fileInfo(index)

        self.textBrowser.setText(file_path)
        self.history_nav.insert(self.nav_index, file_path)

        self.scrollArea.setVisible(True if file_info.isFile() else False)
        # self.wProperties.setVisible(True if file_info.isDir() else False)

        file_name = file_info.fileName()
        if file_name == "" and not file_info.isFile():
            file_name = "Lecteur " + file_path[:-2]
            self.lbl_nom.setText(f"{file_name}")
        else:
            self.lbl_nom.setText(f"Nom: {file_name}")

        self.lbl_chemin.setText(f"Chemin: {file_path}")

        locale = QLocale(QLocale.French, QLocale.France)
        last_modified_date = locale.toString(file_info.lastModified(), "dddd dd MMMM yyyy à hh:mm:ss")
        self.lbl_date.setText(f"Date de modification: {last_modified_date}")

        self.lbl_type.setText(f"Type: {file_info.suffix() if file_info.isFile() else 'Dossier'}")

        if file_info.isFile():

            self.canvas.setVisible(False)
            self.panel_preview.setFixedWidth(self.panel_preview.width())
            self.panel_preview.setFixedHeight(500)
            self.mime_type, _ = mimetypes.guess_type(url=file_path)
            file_size = file_info.size()
            total_size, free_space = self.get_disk_usage(os.path.abspath(os.sep))
            percentage = (file_size / total_size) * 100 if total_size > 0 else 0
            file_size = FileUtils.get_size(file_size)
            self.lbl_taille.setText(f"Taille du fichier : {file_size} ({percentage:.2f}%)")
            self.lbl_preview.setText("")

            self.handle_file_type(self.mime_type, file_path)

        if file_info.isDir():
            if os.path.ismount(file_path):
                total_size, free_space = self.get_disk_usage(file_path)
                directory_size = total_size - free_space
                percentage = (directory_size / total_size) * 100 if total_size > 0 else 0
                self.draw_pie_chart(total_size, free_space)
                total_size = FileUtils.get_size(total_size)
                free_space = FileUtils.get_size(free_space)
                self.lbl_taille.setText(f"Taille totale / dispo : {total_size} / {free_space} ({percentage:.2f}%)")
            else:
                self.lbl_taille.setText(f"Taille du dossier : calcul en cours ...")
                self.calculate_directory_size(file_path)

    def calculate_directory_size(self, path):
        self.worker = DirectorySizeWorker(path)
        self.worker.signals.result.connect(self.display_directory_size)
        self.worker.signals.finished.connect(self.worker_finished)
        self.thread_pool.start(self.worker)

    def display_directory_size(self, size):
        directory_size = size
        root_size, _ = self.get_disk_usage(os.path.abspath(os.sep))
        percentage = (directory_size / root_size) * 100 if root_size > 0 else 0
        self.draw_pie_chart(root_size, directory_size)
        directory_size = FileUtils.get_size(directory_size)
        if size > 0:
            self.lbl_taille.setText(f"Taille du dossier : {directory_size} ({percentage:.2f}%)")
        else:
            self.lbl_taille.setText(f"Taille du dossier : vide")

    def handle_file_type(self, mime_type, file_path):
        self.mime_type = FileUtils.analyze_extension(file_path)

        if self.mime_type:
            if self.mime_type.startswith('text'):
                FileUtils.display_text_file(self.lbl_preview, file_path)
            elif self.mime_type.startswith('image'):
                FileUtils.display_image_file(self.panel_listview, self.lbl_preview, file_path)
            elif self.mime_type.__contains__('pdf'):
                self.lbl_preview.clear()
                FileUtils.display_pdf_file(self.lbl_preview, file_path)

    def worker_finished(self):
        print("Travail fini")

    def get_disk_usage(self, path):
        usage = shutil.disk_usage(path)
        return usage.total, usage.free

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
        self.canvas.setVisible(True)

    def update_lists(self, index):
        self.nav_index = len(self.history_nav) - 1
        self.listView.setRootIndex(index)
        self.infos(index)

    def open_context_menu(self, position):

        sender = self.sender()

        if isinstance(sender, QTreeView):
            indexes = self.treeView.selectedIndexes()
        elif isinstance(sender, QListView):
            indexes = self.listView.selectedIndexes()
        else:
            return

        menu = QMenu()
        new_folder = QAction(QIcon(f"{PATH_ROOT}/toolbar/add-folder.png"), "Nouvel élément", self)
        new_folder.setShortcut("Ctrl+N")
        cut_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/cut.png"), "Couper", self)
        cut_action.setShortcut("Ctrl+X")
        copy_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/copy.png"), "Copier", self)
        copy_action.setShortcut("Ctrl+C")

        rename_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/rename.png"), "Renommer", self)
        copy_action.setShortcut("F2")

        delete_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/remove-folder.png"), "Supprimer", self)
        command_action = QAction(QIcon(f"{PATH_ROOT}/toolbar/running.png"), "Exécuter commande", self)
        new_folder.triggered.connect(self.new_file)
        cut_action.triggered.connect(self.cut_file)
        copy_action.triggered.connect(self.copy_file)
        rename_action.triggered.connect(self.rename_file)
        delete_action.triggered.connect(self.delete_file)
        command_action.triggered.connect(self.execute_command)
        menu.addAction(new_folder)
        menu.addAction(cut_action)
        menu.addAction(copy_action)
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        menu.addAction(command_action)

        menu.exec(QCursor.pos())

    def command_log(self):
        pass

    def center_on_screen(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self_geometry = self.frameGeometry()
        self_geometry.moveCenter(screen_geometry.center())
        self.move(self_geometry.topLeft())


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
