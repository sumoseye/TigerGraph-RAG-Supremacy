# backend/app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    
    # Gemini
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    # TigerGraph Savanah (NEW)
    TIGERGRAPH_HOST: str = os.getenv("TIGERGRAPH_HOST")
    TIGERGRAPH_GRAPH_NAME: str = os.getenv("TIGERGRAPH_GRAPH_NAME")
    TIGERGRAPH_GSQL_SECRET: str = os.getenv("TIGERGRAPH_GSQL_SECRET")
    TIGERGRAPH_REST_PORT: str = os.getenv("TIGERGRAPH_REST_PORT", "443")
    TIGERGRAPH_GS_PORT: str = os.getenv("TIGERGRAPH_GS_PORT", "443")
    
    # Server
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATASET_PATH: Path = BASE_DIR / "dataset"
    
    @property
    def dataset_exists(self) -> bool:
        return self.DATASET_PATH.exists()
    
    def validate(self):
        if not self.GROQ_API_KEY:
            raise ValueError("❌ GROQ_API_KEY not set")
        if not self.GEMINI_API_KEY:
            raise ValueError("❌ GEMINI_API_KEY not set")
        if not self.TIGERGRAPH_HOST:
            raise ValueError("❌ TIGERGRAPH_HOST not set")
        return True

settings = Settings()
settings.validate()