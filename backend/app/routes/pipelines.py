from fastapi import APIRouter, HTTPException
from app.models import QueryRequest, PipelineResponse, BatchResponse
from pipelines.pipeline_1_groq import pipeline_1_llm_only
from pipelines.pipeline_2_rag import pipeline_2_rag
from datetime import datetime

router = APIRouter()

@router.post("/pipeline/llm", response_model=PipelineResponse)
async def run_llm_pipeline(request: QueryRequest):
    try:
        result = await pipeline_1_llm_only(request.query)
        return PipelineResponse(pipeline_name="LLM Only (Groq)", **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipeline/rag", response_model=PipelineResponse)
async def run_rag_pipeline(request: QueryRequest):
    """Pipeline 2: Basic RAG with ChromaDB"""
    try:
        result = await pipeline_2_rag(request.query)
        return PipelineResponse(pipeline_name="Basic RAG (ChromaDB)", **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipeline/tigergraph", response_model=PipelineResponse)
async def run_tigergraph_pipeline(request: QueryRequest):
    return PipelineResponse(
        pipeline_name="TigerGraph",
        answer="🚧 Coming soon!",
        latency_ms=0,
        tokens_in=0,
        tokens_out=0,
        tokens_total=0,
        cost=0.0,
        sources=[],
        reasoning="Not implemented",
        status="pending"
    )

@router.post("/pipelines/all", response_model=BatchResponse)
async def run_all_pipelines(request: QueryRequest):
    try:
        p1_result = await pipeline_1_llm_only(request.query)
        p2_result = await pipeline_2_rag(request.query)
        
        return BatchResponse(
            query=request.query,
            results={
                "llm_only": PipelineResponse(pipeline_name="LLM Only (Groq)", **p1_result),
                "basic_rag": PipelineResponse(pipeline_name="Basic RAG (ChromaDB)", **p2_result),
                "tigergraph": PipelineResponse(
                    pipeline_name="TigerGraph",
                    answer="🚧 Coming soon!",
                    latency_ms=0, tokens_in=0, tokens_out=0, tokens_total=0,
                    cost=0.0, sources=[], reasoning="Not implemented", status="pending"
                )
            },
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "✅ Backend is running",
        "pipelines": {
            "llm_only": "ready",
            "basic_rag": "ready",
            "tigergraph": "coming_soon"
        },
        "api": "Groq Llama 3.1",
        "cost": "$0.00 (FREE)"
    }