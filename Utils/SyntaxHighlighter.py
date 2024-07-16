import json
import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import Qt

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, language_file='langages.json', theme_file='themes.json'):
        super(Highlighter, self).__init__(parent)
        self.parent = parent  # Assurez-vous de stocker une référence au parent
        self.load_languages(language_file)
        self.load_themes(theme_file)
        self.highlighting_rules = []
        self.current_theme = 'dark'
        self.update_styles()

    def load_languages(self, filename):
        with open(filename, 'r') as file:
            self.languages = json.load(file)

    def load_themes(self, filename):
        with open(filename, 'r') as file:
            self.themes = json.load(file)

    def update_styles(self):
        self.styles = self.themes[self.current_theme]
        # Définir le style par défaut pour le parent
        if 'default' in self.styles:
            default_style = self.styles['default']
            background_color = default_style.get('background', {}).get('color', '#FFFFFF')
            text_color = default_style.get('color', '#000000')
            self.parent.setStyleSheet(f"background-color: {background_color}; color: {text_color};")

    def create_format(self, style):
        _format = QTextCharFormat()
        if 'color' in style:
            _format.setForeground(QColor(style['color']))
        if 'font_weight' in style:
            _format.setFontWeight(QFont.Bold if style['font_weight'] == 'bold' else QFont.Normal)
        if 'font_style' in style:
            if style['font_style'] == 'italic':
                _format.setFontItalic(True)
            elif style['font_style'] == 'underline':
                _format.setFontUnderline(True)
        if 'background' in style:
            _format.setBackground(QColor(style['background']))
        return _format

    def set_language(self, language):
        self.highlighting_rules = []

        if language in self.languages:
            rules = self.languages[language]
            if 'keywords' in rules:
                keyword_format = self.create_format(self.styles.get('keyword', {}))
                for pattern in rules['keywords']:
                    self.highlighting_rules.append((re.compile(r'\b' + re.escape(pattern) + r'\b'), keyword_format))
            if 'functions' in rules:
                function_format = self.create_format(self.styles.get('function', {}))
                self.highlighting_rules.append((re.compile(rules['functions']), function_format))
            if 'variables' in rules:
                variable_format = self.create_format(self.styles.get('variable', {}))
                self.highlighting_rules.append((re.compile(rules['variables']), variable_format))

            if 'strings' in rules:
                string_format = self.create_format(self.styles.get('string', {}))
                for pattern in rules['strings']:
                    self.highlighting_rules.append((re.compile(pattern), string_format))
            if 'numbers' in rules:
                number_format = self.create_format(self.styles.get('number', {}))
                self.highlighting_rules.append((re.compile(rules['numbers']), number_format))
            if 'operators' in rules:
                operator_format = self.create_format(self.styles.get('operator', {}))
                self.highlighting_rules.append((re.compile(rules['operators']), operator_format))
            if 'classes' in rules:
                class_format = self.create_format(self.styles.get('class', {}))
                self.highlighting_rules.append((re.compile(rules['classes']), class_format))
            if 'magic_methods' in rules:
                magic_method_format = self.create_format(self.styles.get('magic_method', {}))
                for pattern in rules['magic_methods']:
                    self.highlighting_rules.append((re.compile(r'\b' + re.escape(pattern) + r'\b'), magic_method_format))
            if 'comments' in rules:
                comment_format = self.create_format(self.styles.get('comment', {}))
                self.highlighting_rules.append((re.compile(rules['comments']), comment_format))
            if 'docstrings' in rules:
                docstring_format = self.create_format(self.styles.get('comment', {}))
                for pattern in rules['docstrings']:
                    self.highlighting_rules.append((re.compile(pattern, re.DOTALL), docstring_format))
            if 'parentheses' in rules:
                parentheses_format = self.create_format(self.styles.get('parentheses', {}))
                self.highlighting_rules.append((re.compile(rules['parentheses']), parentheses_format))
            if 'colons' in rules:
                colons_format = self.create_format(self.styles.get('colons', {}))
                self.highlighting_rules.append((re.compile(rules['colons']), colons_format))

    def highlightBlock(self, text):
        for pattern, _format in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), _format)

    def set_theme(self, theme):
        if theme in self.themes:
            self.current_theme = theme
            self.update_styles()
            self.rehighlight()
