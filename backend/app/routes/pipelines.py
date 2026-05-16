from fastapi import APIRouter, HTTPException
from app.models import QueryRequest, PipelineResponse, BatchResponse
from pipelines.pipeline_1_groq import pipeline_1_llm_only
from pipelines.pipeline_2_rag import pipeline_2_rag
from pipelines.pipeline_3_orchestrator import pipeline_3_orchestrator
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
    try:
        result = await pipeline_2_rag(request.query)
        return PipelineResponse(pipeline_name="Basic RAG (ChromaDB)", **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipeline/tigergraph", response_model=PipelineResponse)
async def run_tigergraph_pipeline(request: QueryRequest):
    """Pipeline 3: Multi-Agent Orchestrator with TigerGraph Savanah"""
    try:
        result = await pipeline_3_orchestrator(request.query)
        return PipelineResponse(pipeline_name="Multi-Agent TigerGraph", **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipelines/all", response_model=BatchResponse)
async def run_all_pipelines(request: QueryRequest):
    try:
        p1 = await pipeline_1_llm_only(request.query)
        p2 = await pipeline_2_rag(request.query)
        p3 = await pipeline_3_orchestrator(request.query)
        
        return BatchResponse(
            query=request.query,
            results={
                "llm_only": PipelineResponse(pipeline_name="LLM Only", **p1),
                "basic_rag": PipelineResponse(pipeline_name="Basic RAG", **p2),
                "tigergraph": PipelineResponse(pipeline_name="Multi-Agent TigerGraph", **p3)
            },
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "pipelines": {
            "llm_only": "ready",
            "basic_rag": "ready",
            "tigergraph": "ready"
        }
    }