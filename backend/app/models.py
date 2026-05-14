from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)

class PipelineResponse(BaseModel):
    pipeline_name: str
    answer: str
    latency_ms: float
    tokens_in: int
    tokens_out: int
    tokens_total: int
    cost: float
    sources: List[str]
    reasoning: str
    status: str = "success"
    error: Optional[str] = None

class BatchResponse(BaseModel):
    query: str
    results: dict
    timestamp: str