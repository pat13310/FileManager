import sys
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QLabel
from PySide6.QtGui import QFont, QColor
from Utils.SyntaxHighlighter import Highlighter
import json

class CodeViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.combo_layout = QHBoxLayout()
        self.theme_layout = QHBoxLayout()

        self.lang_selector = QComboBox()
        self.lang_selector.addItems(["python", "javascript"])
        self.lang_selector.currentIndexChanged.connect(self.update_highlighting)

        self.combo_layout.addWidget(QLabel("Select Language:"))
        self.combo_layout.addWidget(self.lang_selector)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["default", "dark", "light"])
        self.theme_selector.currentIndexChanged.connect(self.change_theme)

        self.theme_layout.addWidget(QLabel("Select Theme:"))
        self.theme_layout.addWidget(self.theme_selector)

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Courier", 10))

        self.layout.addLayout(self.combo_layout)
        self.layout.addLayout(self.theme_layout)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

        self.highlighter = Highlighter(self.text_edit.document())

        self.code_samples = {
            "python": '''\
def example_function(param1, param2):
    """This is a docstring."""
    # This is a comment
    if param1 > param2:
        print("param1 is greater than param2")
    else:
        print("param1 is not greater than param2")
''',
            "javascript": '''\
function exampleFunction(param1, param2) {
    // This is a comment
    if (param1 > param2) {
        console.log("param1 is greater than param2");
    } else {
        console.log("param1 is not greater than param2");
    }
}
'''
        }

        self.update_highlighting()

    def update_highlighting(self):
        language = self.lang_selector.currentText()
        code = self.code_samples.get(language, "")
        self.highlighter.set_language(language)
        self.text_edit.setPlainText(code)

    def change_theme(self):
        theme = self.theme_selector.currentText()
        self.highlighter.set_theme(theme)
        self.apply_background_color(theme)
        self.update_highlighting()

    def apply_background_color(self, theme):
        with open('themes.json', 'r') as file:
            themes = json.load(file)
            background_color = themes[theme].get("background", {}).get("color", "#FFFFFF")
            self.text_edit.setStyleSheet(f"background-color: {background_color}; color: {self.get_text_color(background_color)}")

    def get_text_color(self, background_color):
        # Return white text for dark background and black text for light background
        if background_color.lower() in ["#1e1e1e"]:
            return "#FFFFFF"
        return "#000000"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CodeViewer()
    viewer.show()
    sys.exit(app.exec())
