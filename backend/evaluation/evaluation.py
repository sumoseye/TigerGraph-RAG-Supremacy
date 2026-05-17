# backend/app/routes/evaluation.py (CORRECTED)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models import EvaluationResponse
from evaluation.evaluator import evaluate_pipelines, load_results

router = APIRouter()

class EvaluationRequest(BaseModel):
    query: str
    ground_truth: str

@router.post("/evaluate")
async def evaluate(request: EvaluationRequest):
    """
    Evaluate all 3 pipelines using LLM-as-Judge and BERTScore
    """
    try:
        results = await evaluate_pipelines(
            query=request.query,
            ground_truth=request.ground_truth
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/accuracy-report")
async def accuracy_report():
    """
    Get cumulative accuracy report across all evaluations
    """
    try:
        report = load_results()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))