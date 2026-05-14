import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Groq API
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Server
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5174").split(",")
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATASET_PATH: Path = BASE_DIR / "dataset"
    
    @property
    def dataset_exists(self) -> bool:
        return self.DATASET_PATH.exists()
    
    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not set in .env")
        return True

settings = Settings()
settings.validate()