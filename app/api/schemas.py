from pydantic import BaseModel

class ApplyRequest(BaseModel):
    resume: str
    job_description: str


class ApplyResponse(BaseModel):
    match_score: float
    verdict: str
    cover_letter: str
