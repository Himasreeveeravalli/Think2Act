import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-antigravity-ai-2026")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'ecommerce_studio.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gemini API Key (Optional for live LLM extraction)
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

    # Application Modes
    DEFAULT_CURRENCY = "₹"
    DEMO_MODE_DEFAULT = True
