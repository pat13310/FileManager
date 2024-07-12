# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsManagerVAuCoT.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QCheckBox, QDialogButtonBox


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(400, 300)
        icon = QIcon(QIcon.fromTheme("applications-development"))
        SettingsDialog.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(240, 270, 156, 24))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok
        )
        self.checkBox = QCheckBox(SettingsDialog)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setGeometry(QRect(9, 9, 142, 20))
        self.checkBox_2 = QCheckBox(SettingsDialog)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setGeometry(QRect(9, 35, 182, 20))
        self.checkBox_3 = QCheckBox(SettingsDialog)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.setGeometry(QRect(9, 61, 107, 20))

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)

    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(
            QCoreApplication.translate("SettingsDialog", "Cleaner", None)
        )
        self.checkBox.setText(
            QCoreApplication.translate("SettingsDialog", "Confirmer suppression", None)
        )
        self.checkBox_2.setText(
            QCoreApplication.translate(
                "SettingsDialog", " Prot\u00e9ger r\u00e9pertoires syst\u00e8me", None
            )
        )
        self.checkBox_3.setText(
            QCoreApplication.translate("SettingsDialog", "Afficher aper\u00e7u", None)
        )

    # retranslateUi
