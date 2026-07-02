import io
from PyPDF2 import PdfReader
from docx import Document
from app.utils.text_processor import TextProcessor


class DocumentService:
    def __init__(self):
        self.processor = TextProcessor()

    def parse_pdf(self, file_bytes: bytes) -> str:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return self.processor.clean_text(text)

    def parse_docx(self, file_bytes: bytes) -> str:
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([p.text for p in doc.paragraphs])
        return self.processor.clean_text(text)

    def parse_txt(self, file_bytes: bytes) -> str:
        return self.processor.clean_text(file_bytes.decode('utf-8'))


document_service = DocumentService()