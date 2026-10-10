import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "catalog.db"
SEED_JSON_PATH = DATA_DIR / "catalog_seed.json"

# Ollama / Local LLM settings
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3") # or mistral, phi3, etc.
USE_LLM_IF_AVAILABLE = True
