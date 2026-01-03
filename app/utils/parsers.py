from pydantic import BaseModel, Field
from typing import List, Literal

class MatchResult(BaseModel):
    # LLM gives 0–10 (easier for reasoning)
    raw_score: float = Field(..., ge=0, le=10)
    missing_skills: List[str]

class FinalDecision(BaseModel):
    match_score: int           # 0–100
    verdict: Literal["apply", "maybe", "skip"]
    missing_skills: List[str]
