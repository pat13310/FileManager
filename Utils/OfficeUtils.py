from comtypes.client import CreateObject
import os

class OfficeUtils:
    @staticmethod
    def convert_word_to_pdf(docx_path):
        pdf_path = os.path.abspath(docx_path).replace('.docx', '.pdf').replace('.DOCX', '.pdf')
        docx_path = os.path.abspath(docx_path)

        if not os.path.exists(docx_path):
            print(f"Le fichier {docx_path} n'existe pas.")
            return None

        try:
            print(f"Tentative d'ouverture du fichier Word: {docx_path}")
            word = CreateObject('Word.Application')
            word.Visible = False
            doc = word.Documents.Open(docx_path)
            print(f"Document Word ouvert avec succès: {docx_path}")
            doc.SaveAs(pdf_path, FileFormat=17)  # 17 corresponds to wdFormatPDF
            doc.Close()
            word.Quit()
            print(f"Fichier PDF enregistré avec succès: {pdf_path}")
            return pdf_path
        except Exception as e:
            print(f"Erreur lors de la conversion du fichier Word en PDF : {e}")
            return None

    @staticmethod
    def convert_excel_to_pdf(xlsx_path):
        pdf_path = os.path.abspath(xlsx_path).replace('.xlsx', '.pdf').replace('.XLSX', '.pdf')
        xlsx_path = os.path.abspath(xlsx_path)

        if not os.path.exists(xlsx_path):
            print(f"Le fichier {xlsx_path} n'existe pas.")
            return None

        try:
            print(f"Tentative d'ouverture du fichier Excel: {xlsx_path}")
            excel = CreateObject('Excel.Application')
            excel.Visible = False
            wb = excel.Workbooks.Open(xlsx_path)
            print(f"Document Excel ouvert avec succès: {xlsx_path}")
            wb.ExportAsFixedFormat(0, pdf_path)  # 0 corresponds to xlTypePDF
            wb.Close()
            excel.Quit()
            print(f"Fichier PDF enregistré avec succès: {pdf_path}")
            return pdf_path
        except Exception as e:
            print(f"Erreur lors de la conversion du fichier Excel en PDF : {e}")
            return None

    @staticmethod
    def check_word_installation():
        try:
            word = CreateObject('Word.Application')
            word.Visible = False
            doc = word.Documents.Add()
            doc.Close()
            word.Quit()
            print("Microsoft Word est correctement installé et accessible.")
            return True
        except Exception as e:
            print(f"Erreur lors de l'ouverture de Microsoft Word : {e}")
            return False
