import os
import re
from pathlib import Path
from config.settings import settings

def validate_uploaded_file(file_path: str) -> tuple[bool, str]:
    """
    Validates the uploaded document path, extension, and file size.
    Returns (is_valid, error_message).
    """
    if not file_path:
        return False, "No file uploaded. Please select a document to analyze."
    
    path = Path(file_path)
    if not path.is_file():
        return False, f"File not found: {path.name}"
    
    ext = path.suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        allowed_str = ", ".join(settings.ALLOWED_EXTENSIONS)
        return False, f"Unsupported file type '{ext}'. Allowed formats: {allowed_str}"
    
    file_size_mb = path.stat().st_size / (1024 * 1024)
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        return False, f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed limit of {settings.MAX_FILE_SIZE_MB} MB."
    
    return True, ""

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes filename to prevent directory traversal and illegal characters.
    """
    clean_name = os.path.basename(filename)
    clean_name = re.sub(r'[^\w\s\.-]', '_', clean_name)
    return clean_name
