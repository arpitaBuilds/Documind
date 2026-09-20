import pymupdf as fitz
import docx
from pathlib import Path
from utils.validators import validate_uploaded_file, sanitize_filename

class DocumentProcessor:
    """Extracts text content and metadata from PDF, DOCX, and TXT files."""

    MAX_CHAR_LIMIT = 15000  # Truncates extra long documents for LLM processing

    @classmethod
    def extract_text_and_metadata(cls, file_path: str) -> dict:
        """
        Reads document and returns structured content dictionary:
        {
            "filename": str,
            "file_type": str,
            "text": str,
            "char_count": int,
            "page_count": int,
            "file_size_kb": float
        }
        """
        is_valid, error_msg = validate_uploaded_file(file_path)
        if not is_valid:
            raise ValueError(error_msg)

        path = Path(file_path)
        filename = sanitize_filename(path.name)
        ext = path.suffix.lower()
        file_size_kb = round(path.stat().st_size / 1024, 2)

        text = ""
        page_count = 1

        if ext == ".pdf":
            text, page_count = cls._extract_pdf(file_path)
        elif ext == ".docx":
            text, page_count = cls._extract_docx(file_path)
        elif ext == ".txt":
            text = cls._extract_txt(file_path)
            page_count = 1
        else:
            raise ValueError(f"Unsupported format: {ext}")

        text_clean = text.strip()
        if not text_clean:
            raise ValueError("The uploaded document is empty or contains no readable text.")

        # Truncate if exceeds max character limit
        is_truncated = len(text_clean) > cls.MAX_CHAR_LIMIT
        if is_truncated:
            text_clean = text_clean[:cls.MAX_CHAR_LIMIT] + "\n\n[... Document Truncated for AI Analysis ...]"

        return {
            "filename": filename,
            "file_type": ext.replace(".", "").upper(),
            "text": text_clean,
            "char_count": len(text_clean),
            "page_count": page_count,
            "file_size_kb": file_size_kb,
            "is_truncated": is_truncated
        }

    @staticmethod
    def _extract_pdf(file_path: str) -> tuple[str, int]:
        """Extracts text from PDF using PyMuPDF (fitz)."""
        doc = fitz.open(file_path)
        page_count = len(doc)
        text_pages = []
        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text_pages.append(page_text)
        doc.close()
        return "\n\n".join(text_pages), page_count

    @staticmethod
    def _extract_docx(file_path: str) -> tuple[str, int]:
        """Extracts text from Microsoft Word DOCX."""
        doc = docx.Document(file_path)
        full_text = [p.text for p in doc.paragraphs if p.text.strip()]
        # Estimate page count (~300 words per page)
        word_count = sum(len(p.split()) for p in full_text)
        estimated_pages = max(1, word_count // 300)
        return "\n".join(full_text), estimated_pages

    @staticmethod
    def _extract_txt(file_path: str) -> str:
        """Extracts text from plain text TXT file using UTF-8 encoding with fallback."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
