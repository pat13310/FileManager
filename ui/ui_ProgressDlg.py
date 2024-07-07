# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progressDlgiRPWeU.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QProgressBar, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_progressDlg(object):
    def setupUi(self, progressDlg):
        if not progressDlg.objectName():
            progressDlg.setObjectName(u"progressDlg")
        progressDlg.resize(530, 133)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(progressDlg.sizePolicy().hasHeightForWidth())
        progressDlg.setSizePolicy(sizePolicy)
        progressDlg.setMinimumSize(QSize(0, 0))
        icon = QIcon(QIcon.fromTheme(u"edit-find"))
        progressDlg.setWindowIcon(icon)
        progressDlg.setStyleSheet(u"background-color: rgb(244, 244, 244);")
        progressDlg.setModal(False)
        self.verticalLayout = QVBoxLayout(progressDlg)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_action = QLabel(progressDlg)
        self.lbl_action.setObjectName(u"lbl_action")
        self.lbl_action.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout.addWidget(self.lbl_action)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(progressDlg)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy1)
        self.progressBar.setMaximumSize(QSize(16777215, 16777215))
        self.progressBar.setStyleSheet(u" QProgressBar {\n"
"                border: 1px solid grey;\n"
"                border-radius: 4px;           \n"
"height:8px;        \n"
"margin: 4px;      \n"
"				 \n"
"           }\n"
"  QProgressBar::chunk {\n"
"                background-color:qlineargradient(spread:reflect, x1:0.511416, y1:0.506, x2:0.507, y2:0.0568182, stop:0 rgba(25, 178, 255, 255), stop:1 rgba(66, 131, 197, 255));\n"
"\n"
"                \n"
"				 \n"
"            }\n"
" ")
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(Qt.Orientation.Horizontal)
        self.progressBar.setInvertedAppearance(False)

        self.horizontalLayout.addWidget(self.progressBar)

        self.lblPercent = QLabel(progressDlg)
        self.lblPercent.setObjectName(u"lblPercent")

        self.horizontalLayout.addWidget(self.lblPercent)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.lblMessage = QLabel(progressDlg)
        self.lblMessage.setObjectName(u"lblMessage")
        font = QFont()
        font.setPointSize(8)
        self.lblMessage.setFont(font)

        self.verticalLayout.addWidget(self.lblMessage)


        self.retranslateUi(progressDlg)

        QMetaObject.connectSlotsByName(progressDlg)
    # setupUi

    def retranslateUi(self, progressDlg):
        progressDlg.setWindowTitle(QCoreApplication.translate("progressDlg", u"Dialog", None))
        self.lbl_action.setText(QCoreApplication.translate("progressDlg", u"  Nettoyage en cours ...", None))
        self.lblPercent.setText(QCoreApplication.translate("progressDlg", u"24%", None))
        self.lblMessage.setText(QCoreApplication.translate("progressDlg", u"...", None))
    # retranslateUi

