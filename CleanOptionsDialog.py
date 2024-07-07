import json
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox,
                               QCheckBox, QLabel, QPushButton, QApplication, QGridLayout)


class CleanOptionsDialog(QDialog):
    def __init__(self, json_file):
        super().__init__()
        self.json_file = json_file
        self.check_boxes = {}

        self.setWindowTitle("Configuration Options")
        with open(self.json_file, 'r', encoding="utf-8") as file:
            self.config_data = json.load(file)
        self.main_layout = QVBoxLayout(self)  # Créez et assignez un QVBoxLayout à la dialog
        self.build_form(self.config_data)

    def build_form(self, config_data):
        for category, data in config_data['Configurations'].items():
            group_box = QGroupBox(data['description'])
            grid_layout = QGridLayout(group_box)  # Créez et assignez un QGridLayout au group_box

            row = 0
            col = 0
            for key, option in data['options'].items():
                check_box = QCheckBox(option['label'])
                check_box.setChecked(option['enabled'])
                grid_layout.addWidget(check_box, row, col)  # Ajoutez check_box au grid_layout

                safe_key = key.replace(" ", "_")
                self.check_boxes[safe_key] = check_box

                col += 1
                if col > 1:  # Si vous avez rempli deux colonnes, réinitialisez pour la nouvelle ligne
                    col = 0
                    row += 1

            self.main_layout.addWidget(group_box)  # Ajoutez group_box au main_layout

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_config)
        self.main_layout.addWidget(save_button)  # Ajoutez save_button au main_layout

    def save_config(self):
        for section_name, section_info in self.config_data['Configurations'].items():
            for option_key, option_info in section_info['options'].items():
                check_box = self.check_boxes[option_key]
                option_info['enabled'] = check_box.isChecked()  # Mettre à jour les données de configuration

        # Sauvegarder dans le fichier JSON
        with open(self.json_file, 'w', encoding='utf-8') as file:
            json.dump(self.config_data, file, ensure_ascii=False, indent=4)
        self.accept()


# Main application
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    dialog = ScannerOptionsDialog('scanner.json')
    dialog.exec()
