# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FileManagerXeEPWL.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QListView, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QSplitter,
    QStatusBar, QTextBrowser, QToolBar, QToolButton,
    QTreeView, QVBoxLayout, QWidget)

class Ui_FileManager(object):
    def setupUi(self, FileManager):
        if not FileManager.objectName():
            FileManager.setObjectName(u"FileManager")
        FileManager.resize(1326, 658)
        FileManager.setUnifiedTitleAndToolBarOnMac(False)
        self.actionNouveau = QAction(FileManager)
        self.actionNouveau.setObjectName(u"actionNouveau")
        self.actionCopier = QAction(FileManager)
        self.actionCopier.setObjectName(u"actionCopier")
        self.actionCouper = QAction(FileManager)
        self.actionCouper.setObjectName(u"actionCouper")
        self.actionColler = QAction(FileManager)
        self.actionColler.setObjectName(u"actionColler")
        self.actionSauvegarder = QAction(FileManager)
        self.actionSauvegarder.setObjectName(u"actionSauvegarder")
        self.actionRenommer = QAction(FileManager)
        self.actionRenommer.setObjectName(u"actionRenommer")
        self.centralwidget = QWidget(FileManager)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 32))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 2, 0, 2)
        self.btn_prev = QToolButton(self.widget)
        self.btn_prev.setObjectName(u"btn_prev")
        self.btn_prev.setMinimumSize(QSize(32, 32))
        icon = QIcon(QIcon.fromTheme(u"go-previous"))
        self.btn_prev.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_prev)

        self.btn_next = QToolButton(self.widget)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setMinimumSize(QSize(32, 32))
        self.btn_next.setMaximumSize(QSize(16777215, 32))
        icon1 = QIcon(QIcon.fromTheme(u"go-next"))
        self.btn_next.setIcon(icon1)

        self.horizontalLayout.addWidget(self.btn_next)

        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QSize(0, 32))
        self.textBrowser.setMaximumSize(QSize(16777215, 32))

        self.horizontalLayout.addWidget(self.textBrowser)


        self.verticalLayout_3.addWidget(self.widget)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setFrameShape(QFrame.Shape.StyledPanel)
        self.splitter.setLineWidth(1)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.panel_treeview = QWidget(self.splitter)
        self.panel_treeview.setObjectName(u"panel_treeview")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.panel_treeview.sizePolicy().hasHeightForWidth())
        self.panel_treeview.setSizePolicy(sizePolicy1)
        self.panel_treeview.setStyleSheet(u"background-color: white;")
        self.verticalLayout_2 = QVBoxLayout(self.panel_treeview)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.treeView = QTreeView(self.panel_treeview)
        self.treeView.setObjectName(u"treeView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy2)
        self.treeView.setMinimumSize(QSize(420, 0))
        self.treeView.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: black;")
        self.treeView.setTabKeyNavigation(True)
        self.treeView.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

        self.verticalLayout_2.addWidget(self.treeView)

        self.splitter.addWidget(self.panel_treeview)
        self.panel_listview = QWidget(self.splitter)
        self.panel_listview.setObjectName(u"panel_listview")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.panel_listview.sizePolicy().hasHeightForWidth())
        self.panel_listview.setSizePolicy(sizePolicy3)
        self.verticalLayout = QVBoxLayout(self.panel_listview)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.listView = QListView(self.panel_listview)
        self.listView.setObjectName(u"listView")
        self.listView.setAcceptDrops(True)
        self.listView.setFrameShape(QFrame.Shape.VLine)

        self.verticalLayout.addWidget(self.listView)

        self.splitter.addWidget(self.panel_listview)
        self.panel_preview = QWidget(self.splitter)
        self.panel_preview.setObjectName(u"panel_preview")
        sizePolicy1.setHeightForWidth(self.panel_preview.sizePolicy().hasHeightForWidth())
        self.panel_preview.setSizePolicy(sizePolicy1)
        self.panel_preview.setMinimumSize(QSize(300, 0))
        self.panel_preview.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.verticalLayout_4 = QVBoxLayout(self.panel_preview)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.lbl_preview = QLabel(self.panel_preview)
        self.lbl_preview.setObjectName(u"lbl_preview")
        self.lbl_preview.setStyleSheet(u"background-color: rgb(0, 0, 0);")

        self.verticalLayout_4.addWidget(self.lbl_preview)

        self.wProperties = QWidget(self.panel_preview)
        self.wProperties.setObjectName(u"wProperties")
        self.verticalLayout_5 = QVBoxLayout(self.wProperties)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lbl_nom = QLabel(self.wProperties)
        self.lbl_nom.setObjectName(u"lbl_nom")
        self.lbl_nom.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_5.addWidget(self.lbl_nom)

        self.lbl_chemin = QLabel(self.wProperties)
        self.lbl_chemin.setObjectName(u"lbl_chemin")
        self.lbl_chemin.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_5.addWidget(self.lbl_chemin)

        self.lbl_taille = QLabel(self.wProperties)
        self.lbl_taille.setObjectName(u"lbl_taille")
        self.lbl_taille.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_5.addWidget(self.lbl_taille)

        self.lbl_date = QLabel(self.wProperties)
        self.lbl_date.setObjectName(u"lbl_date")
        self.lbl_date.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_5.addWidget(self.lbl_date)

        self.lbl_type = QLabel(self.wProperties)
        self.lbl_type.setObjectName(u"lbl_type")
        self.lbl_type.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.verticalLayout_5.addWidget(self.lbl_type)


        self.verticalLayout_4.addWidget(self.wProperties)

        self.splitter.addWidget(self.panel_preview)

        self.verticalLayout_3.addWidget(self.splitter)

        FileManager.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(FileManager)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1326, 33))
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        FileManager.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(FileManager)
        self.statusbar.setObjectName(u"statusbar")
        FileManager.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(FileManager)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMinimumSize(QSize(0, 32))
        FileManager.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menuFichier.addAction(self.actionNouveau)
        self.menuFichier.addAction(self.actionCopier)
        self.menuFichier.addAction(self.actionCouper)
        self.menuFichier.addAction(self.actionColler)
        self.menuFichier.addAction(self.actionRenommer)
        self.menuFichier.addAction(self.actionSauvegarder)

        self.retranslateUi(FileManager)

        QMetaObject.connectSlotsByName(FileManager)
    # setupUi

    def retranslateUi(self, FileManager):
        FileManager.setWindowTitle(QCoreApplication.translate("FileManager", u"FileManager", None))
        self.actionNouveau.setText(QCoreApplication.translate("FileManager", u"Nouveau", None))
        self.actionCopier.setText(QCoreApplication.translate("FileManager", u"Copier", None))
        self.actionCouper.setText(QCoreApplication.translate("FileManager", u"Couper", None))
        self.actionColler.setText(QCoreApplication.translate("FileManager", u"Coller", None))
        self.actionSauvegarder.setText(QCoreApplication.translate("FileManager", u"Sauvegarder", None))
        self.actionRenommer.setText(QCoreApplication.translate("FileManager", u"Renommer", None))
        self.btn_prev.setText(QCoreApplication.translate("FileManager", u"...", None))
        self.btn_next.setText(QCoreApplication.translate("FileManager", u"...", None))
        self.lbl_preview.setText(QCoreApplication.translate("FileManager", u"TextLabel", None))
        self.lbl_nom.setText(QCoreApplication.translate("FileManager", u"Nom", None))
        self.lbl_chemin.setText(QCoreApplication.translate("FileManager", u"Chemin", None))
        self.lbl_taille.setText(QCoreApplication.translate("FileManager", u"Taille", None))
        self.lbl_date.setText(QCoreApplication.translate("FileManager", u"Date de modification", None))
        self.lbl_type.setText(QCoreApplication.translate("FileManager", u"Type", None))
        self.menuFichier.setTitle(QCoreApplication.translate("FileManager", u"Fichier", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("FileManager", u"toolBar", None))
    # retranslateUi

