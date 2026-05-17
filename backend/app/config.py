# backend/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the backend directory
BASE_DIR = Path(__file__).resolve().parent.parent  # ✅ Add .resolve()

# Load .env from backend directory
env_file = BASE_DIR / ".env"
print(f"\nLoading .env from: {env_file}")
print(f".env exists: {env_file.exists()}")

load_dotenv(dotenv_path=env_file, override=True)

class Settings:
    # Groq API
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Hugging Face
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    HF_JUDGE_MODEL: str = "meta-llama/Llama-3.1-8B-Instruct"
    
    # Server
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "9000"))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5174,http://localhost:3000").split(",")
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    DATASET_PATH: Path = BASE_DIR / "dataset"
    EVALUATION_PATH: Path = BASE_DIR / "evaluation"
    
    @property
    def dataset_exists(self) -> bool:
        return self.DATASET_PATH.exists()

settings = Settings()

# ✅ ADD THESE DEBUG LINES
print(f"GROQ_API_KEY loaded: {bool(settings.GROQ_API_KEY)}")
print(f"HF_TOKEN loaded: {bool(settings.HF_TOKEN)}")
if settings.HF_TOKEN:
    print(f"HF_TOKEN: {settings.HF_TOKEN[:20]}...")
print(f"EVALUATION_PATH: {settings.EVALUATION_PATH}")
print(f"EVALUATION_PATH exists: {settings.EVALUATION_PATH.exists()}")
print()  # ✅ Empty line for spacing