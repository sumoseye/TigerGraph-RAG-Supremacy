# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import pipelines

# Import evaluation at startup to initialize HF tools
print("\nInitializing evaluation module...")
try:
    from evaluation import evaluator
    print("✅ Evaluation module loaded")
except Exception as e:
    print(f"⚠️  Evaluation module error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "="*70)
    print("RESEARCH PIPELINE BATTLE")
    print("="*70)
    print(f"API: Groq {settings.GROQ_MODEL}")
    print(f"Dataset: {settings.DATASET_PATH}")
    print(f"Dataset Exists: {settings.dataset_exists}")
    print(f"HF Token Loaded: {bool(settings.HF_TOKEN)}")
    print("="*70 + "\n")
    
    yield
    
    print("\nShutting down server...")

app = FastAPI(
    title="Research Pipeline Battle API",
    description="Compare research pipeline approaches",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pipelines.router, prefix="/api", tags=["pipelines"])

@app.get("/")
async def root():
    return {
        "message": "Research Pipeline Battle API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health",
            "pipelines": "/api/pipelines/all"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.BACKEND_PORT)