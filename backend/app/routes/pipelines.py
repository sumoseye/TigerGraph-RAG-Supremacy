# backend/app/routes/pipelines.py
from fastapi import APIRouter, HTTPException
from app.models import QueryRequest, PipelineResponse, BatchResponse
from pipelines.pipeline_1_groq import pipeline_1_llm_only
from pipelines.pipeline_2_rag import pipeline_2_rag
from pipelines.pipeline_3_agentic import pipeline_3_agentic
from datetime import datetime
import asyncio

router = APIRouter()


@router.post("/pipeline/llm", response_model=PipelineResponse)
async def run_llm_pipeline(request: QueryRequest):
    try:
        result = await pipeline_1_llm_only(request.query)
        return PipelineResponse(pipeline_name="LLM Only", **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipeline/rag", response_model=PipelineResponse)
async def run_rag_pipeline(request: QueryRequest):
    try:
        result = await pipeline_2_rag(request.query)
        return PipelineResponse(pipeline_name="Basic RAG", **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipeline/agentic", response_model=PipelineResponse)
async def run_agentic_pipeline(request: QueryRequest):
    try:
        result = await pipeline_3_agentic(request.query)
        return PipelineResponse(pipeline_name="Multi-Agent", **result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipelines/all", response_model=BatchResponse)
async def run_all_pipelines(request: QueryRequest):
    """Run all 3 pipelines AND evaluate them"""
    try:
        print(f"\n{'='*70}")
        print(f"Running all pipelines for: {request.query}")
        print(f"{'='*70}")

        # Step 1: Run all pipelines
        print("\n⏳ Running Pipeline 1 (LLM Only)...")
        p1 = await pipeline_1_llm_only(request.query)
        print(f"✅ Pipeline 1 complete - {p1['tokens_total']} tokens")

        print("\n⏳ Running Pipeline 2 (RAG)...")
        p2 = await pipeline_2_rag(request.query)
        print(f"✅ Pipeline 2 complete - {p2['tokens_total']} tokens")

        print("\n⏳ Running Pipeline 3 (GraphRAG)...")
        p3 = await pipeline_3_agentic(request.query)
        print(f"✅ Pipeline 3 complete - {p3['tokens_total']} tokens")

        # Step 2: Evaluate
        print(f"\n⏳ Evaluating pipelines...")

        from evaluation.evaluator import evaluate_pipeline_results

        try:
            eval_results = await asyncio.wait_for(
                evaluate_pipeline_results(
                    query=request.query,
                    p1_answer=p1["answer"],
                    p2_answer=p2["answer"],
                    p3_answer=p3["answer"]
                ),
                timeout=120.0
            )
            print(f"✅ Evaluation complete")
        except asyncio.TimeoutError:
            print("⚠️  Evaluation timed out")
            eval_results = {
                "llm_judge_p1": None, "llm_judge_p2": None, "llm_judge_p3": None,
                "bertscore_p1": None, "bertscore_p2": None, "bertscore_p3": None,
            }
        except Exception as e:
            print(f"⚠️  Evaluation error: {e}")
            eval_results = {
                "llm_judge_p1": None, "llm_judge_p2": None, "llm_judge_p3": None,
                "bertscore_p1": None, "bertscore_p2": None, "bertscore_p3": None,
            }

        # Step 3: Create responses
        p1_response = PipelineResponse(pipeline_name="LLM Only", **p1)
        p1_response.accuracy_judge = eval_results["llm_judge_p1"]
        p1_response.accuracy_bertscore = eval_results["bertscore_p1"]

        p2_response = PipelineResponse(pipeline_name="Basic RAG", **p2)
        p2_response.accuracy_judge = eval_results["llm_judge_p2"]
        p2_response.accuracy_bertscore = eval_results["bertscore_p2"]

        p3_response = PipelineResponse(pipeline_name="Multi-Agent", **p3)
        p3_response.accuracy_judge = eval_results["llm_judge_p3"]
        p3_response.accuracy_bertscore = eval_results["bertscore_p3"]

        print(f"\n✅ RETURNING RESULTS TO FRONTEND\n")

        return BatchResponse(
            query=request.query,
            results={
                "llm_only": p1_response,
                "basic_rag": p2_response,
                "tigergraph": p3_response
            },
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "pipelines": {
            "llm_only": "ready",
            "basic_rag": "ready",
            "agentic": "ready"
        }
    }