from typing import TypedDict, List

class AgentState(TypedDict):
    resume: str
    job_description: str
    match_score: int
    verdict: str
    missing_skills: List[str]
    cover_letter: str
