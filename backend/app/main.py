from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import pipelines

app = FastAPI(
    title="Research Pipeline Battle API",
    description="Compare research pipeline approaches",
    version="1.0.0"
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
        "message": "🚀 Research Pipeline Battle API",
        "version": "1.0.0",
        "dataset_loaded": settings.dataset_exists,
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health",
            "pipeline_1": "/api/pipeline/llm",
            "run_all": "/api/pipelines/all"
        }
    }

@app.on_event("startup")
async def startup():
    print("\n" + "="*70)
    print("🚀 RESEARCH PIPELINE BATTLE")
    print("="*70)
    print(f"✅ API: Groq Llama 3.1")
    print(f"✅ Dataset: {settings.DATASET_PATH}")
    print(f"✅ Dataset Exists: {settings.dataset_exists}")
    print("="*70 + "\n")