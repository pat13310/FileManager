import json
import mimetypes
from enum import Enum

import chardet
import fitz
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QLabel
from psd_tools import PSDImage


class FileFormat(Enum):
    PDF = 17
    DOCX = 16
    HTML = 8
    TEXT = 2
    RTF = 6


class FileUtils:
    @staticmethod
    def analyze_extension(file_path: str, json_path="mime_types.json"):
        mime_type = None
        parts = file_path.split(".")

        if len(parts) >= 2:
            ext = parts[-1].lower()  # Assurez-vous que l'extension est en minuscule
            try:
                with open(json_path, "r") as file:
                    mime_types = json.load(file)
                mime_type = mime_types.get(ext)
            except FileNotFoundError:
                print(f"Le fichier {json_path} n'a pas été trouvé.")

        if not mime_type:
            mime_type, _ = mimetypes.guess_type(file_path)

        return mime_type

    @staticmethod
    def display_text_file(label: QLabel, file_path, encoding="utf-8"):
        with open(file_path, "r", encoding=encoding) as file:
            content = file.read()
        label.clear()
        label.setStyleSheet("color: black")
        label.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        label.setText(content)

    @staticmethod
    def display_image_file(parent, label: QLabel, file_path: str):
        pixmap = QPixmap(file_path)
        label.setScaledContents(False)
        label.setAlignment(Qt.AlignCenter)
        if parent.width() <= pixmap.width() or parent.height() <= pixmap.height():
            pixmap = pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio)

        label.clear()
        label.setPixmap(pixmap)

    @staticmethod
    def display_pdf_file(label: QLabel, file_path):
        doc = fitz.open(file_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        img = QImage(
            pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888
        )
        pixmap = QPixmap.fromImage(img)
        label.setPixmap(pixmap)
        # label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))
        doc.close()

    # @staticmethod
    # def diplay_word_file(label: QLabel, file):
    #     file_base = file.split('.')[0]
    #     pdf_file = file_base + '.pdf'
    #     FileUtils.convert_docx_to_pdf(file, pdf_file)
    #     FileUtils.display_pdf_file(label, pdf_file)
    #     os.remove(pdf_file)

    @staticmethod
    def get_size(size, decimal_places=2) -> str:
        for unit in ["Octets", "Ko", "Mo", "Go", "To", "Po"]:
            if size < 1024.0:
                return f"{size:.{decimal_places}f} {unit}"
            size /= 1024.0
        return f"{size:.{decimal_places}f} Eo"  # Si size est très grand, retourner en exa-octets

    @staticmethod
    def detect_file_encoding(file_path):
        with open(file_path, "rb") as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding: str | None | float = result["encoding"]
            confidence = result["confidence"]
        print(f"Detected encoding: {encoding} with confidence {confidence}")
        return encoding.lower()

    @staticmethod
    def display_psd(parent, label:QLabel,file_name):
        psd = PSDImage.open(file_name)

        # Composite the PSD image
        image = psd.composite()
        image = image.convert("RGBA")  # Ensure the image is in RGBA format

        # Convert to QImage
        data = image.tobytes("raw", "RGBA")
        q_image = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(q_image)
        label.setAlignment(Qt.AlignCenter)
        if parent.width() <= pixmap.width() or parent.height() <= pixmap.height():
            pixmap = pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio)

        label.clear()
        label.setPixmap(pixmap)
        # Display the QPixmap in QLabel
        label.setPixmap(pixmap)
        label.adjustSize()


if __name__ == "__main__":
    file_path = "../requirements.txt"
    encoding = FileUtils.detect_file_encoding(file_path)
    pass
