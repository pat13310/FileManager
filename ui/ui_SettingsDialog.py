# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsManagerVAuCoT.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QSizePolicy, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(400, 300)
        icon = QIcon(QIcon.fromTheme(u"applications-development"))
        SettingsDialog.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(240, 270, 156, 24))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.checkBox = QCheckBox(SettingsDialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(9, 9, 142, 20))
        self.checkBox_2 = QCheckBox(SettingsDialog)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(9, 35, 182, 20))
        self.checkBox_3 = QCheckBox(SettingsDialog)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setGeometry(QRect(9, 61, 107, 20))

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Cleaner", None))
        self.checkBox.setText(QCoreApplication.translate("SettingsDialog", u"Confirmer suppression", None))
        self.checkBox_2.setText(QCoreApplication.translate("SettingsDialog", u" Prot\u00e9ger r\u00e9pertoires syst\u00e8me", None))
        self.checkBox_3.setText(QCoreApplication.translate("SettingsDialog", u"Afficher aper\u00e7u", None))
    # retranslateUi

