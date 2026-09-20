import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of the Project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Settings:
    """DocuMind Configuration Settings loaded from Environment Variables."""
    
    BASE_DIR: Path = BASE_DIR

    # Langflow API Settings

    LANGFLOW_URL: str = os.getenv("LANGFLOW_URL", "http://localhost:7860")
    LANGFLOW_FLOW_ID: str = os.getenv("LANGFLOW_FLOW_ID", "")
    LANGFLOW_API_KEY: str = os.getenv("LANGFLOW_API_KEY", "")
    
    # Langflow Superuser Auth Credentials
    LANGFLOW_SUPERUSER: str = os.getenv("LANGFLOW_SUPERUSER", "admin")
    LANGFLOW_SUPERUSER_PASSWORD: str = os.getenv("LANGFLOW_SUPERUSER_PASSWORD", "adminpassword123")
    
    # JWT Security Settings
    LANGFLOW_SECRET_KEY: str = os.getenv("LANGFLOW_SECRET_KEY", "default-secret-key-change-in-prod")
    LANGFLOW_ALGORITHM: str = os.getenv("LANGFLOW_ALGORITHM", "HS256")
    
    # Application Limits & Settings
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    ALLOWED_EXTENSIONS: set = set(
        os.getenv("ALLOWED_EXTENSIONS", ".pdf,.docx,.txt").lower().split(",")
    )
    
    # Enable robust fallback mode if Langflow server is offline/not configured (Default: False)
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "t")

    # Standardized Taxonomy Categories for Consistent Prompting & Validation
    TAXONOMY_CATEGORIES: list = [
        "Education & Tech",
        "Research & Academia",
        "Career & HR",
        "Finance & Banking",
        "Legal & Compliance",
        "Business & Strategy",
        "Healthcare & Medical",
        "Personal & Official",
        "General & Miscellaneous"
    ]

settings = Settings()

