import io
import json
import mimetypes

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage, QPainter
from PySide6.QtWidgets import QLabel, QWidget
import chardet
# from pdf2image import convert_from_path
import fitz
from pypdf import PdfReader
from PIL import Image


class FileUtils:

    @staticmethod
    def analyze_extension(file_path, json_path='mime_types.json'):
        mime_type = None
        parts = file_path.split('.')

        if len(parts) >= 2:
            ext = parts[-1].lower()  # Assurez-vous que l'extension est en minuscule
            try:
                with open(json_path, 'r') as file:
                    mime_types = json.load(file)
                mime_type = mime_types.get(ext)
            except FileNotFoundError:
                print(f"Le fichier {json_path} n'a pas été trouvé.")

        if not mime_type:
            mime_type, _ = mimetypes.guess_type(file_path)

        return mime_type

    @staticmethod
    def display_text_file(label: QLabel, file_path, encoding='utf-8'):
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
        label.clear()
        label.setStyleSheet("color: black")
        label.setText(content)

    @staticmethod
    def display_image_file(parent, label: QLabel, file_path: str):
        pixmap = QPixmap(file_path)
        if parent.width() <= pixmap.width() or parent.height() <= pixmap.height():
            # pixmap = pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2, Qt.KeepAspectRatio)
            pixmap = pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio)
            label.setScaledContents(True)
            label.setAlignment(Qt.AlignCenter)
        else:
            label.setScaledContents(False)
            label.setAlignment(Qt.AlignCenter)

        label.clear()
        label.setPixmap(pixmap)

    @staticmethod
    def display_pdf_file(label: QLabel, file_path):
        doc = fitz.open(file_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        label.setPixmap(pixmap)
        #label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))
        doc.close()
    @staticmethod
    def diplay_pdf_arch(label: QLabel, file):
        pdf_document = fitz.open(file)
        # Extraire la première page en tant qu'image
        page = pdf_document.load_page(0)  # Numérotation des pages commence à 0
        pix = page.get_pixmap()

        # Convertir le pixmap en image Qt
        image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(image)
        label.setPixmap(pixmap)

        # Centrez le pixmap dans le QLabel
        label.setAlignment(Qt.AlignCenter)


    @staticmethod
    def get_size(size, decimal_places=2) -> str:
        for unit in ['Octets', 'Ko', 'Mo', 'Go', 'To', 'Po']:
            if size < 1024.0:
                return f"{size:.{decimal_places}f} {unit}"
            size /= 1024.0
        return f"{size:.{decimal_places}f} Eo"  # Si size est très grand, retourner en exa-octets

    @staticmethod
    def detect_file_encoding(file_path):
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding: str | None | float = result['encoding']
            confidence = result['confidence']
        print(f"Detected encoding: {encoding} with confidence {confidence}")
        return encoding.lower()


if __name__ == '__main__':
    file_path = '../requirements.txt'
    encoding = FileUtils.detect_file_encoding(file_path)
    pass
