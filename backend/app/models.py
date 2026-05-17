from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class QueryRequest(BaseModel):
    query: str

class PipelineResponse(BaseModel):
    pipeline_name: str
    answer: str
    latency_ms: float
    tokens_in: int
    tokens_out: int
    tokens_total: int
    sources: List[str]
    cost: float
    reasoning: str
    status: str
    accuracy_judge: bool | None = None
    accuracy_bertscore: float | None = None
class BatchResponse(BaseModel):
    query: str
    results: Dict[str, PipelineResponse]
    timestamp: str