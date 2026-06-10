from pydantic import BaseModel, Field
from typing import Optional


class DetectRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=50000)


class SentenceScore(BaseModel):
    text: str
    score: float  # 0-100 AI probability


class MetricDetail(BaseModel):
    score: float          # 0-100
    label: str
    description: str
    weight: float


class DetectResponse(BaseModel):
    score: float          # 0-100 overall AI probability
    verdict: str          # "Human Written" | "Likely Human" | "Uncertain" | "Likely AI" | "AI Generated"
    confidence: str       # "Low" | "Medium" | "High" | "Very High"
    breakdown: dict[str, MetricDetail]
    ai_phrases_found: list[str]
    sentences: list[SentenceScore]
    stats: dict
    warning: Optional[str] = None


class HumanizeRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=10000)
    intensity: str = Field(default="balanced", pattern="^(subtle|balanced|aggressive)$")
    mode: str = Field(default="ai", pattern="^(ai|rules)$")


class HumanizeResponse(BaseModel):
    original: str
    humanized: str
    changes_made: list[str]
    estimated_ai_score: float
    original_ai_score: Optional[float] = None
