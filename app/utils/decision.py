from app.utils.parsers import FinalDecision

def decide(raw_score: float, missing_skills: list[str]) -> FinalDecision:
    """
    Convert raw LLM score (0–10) into production-safe decision.
    """

    normalized = int((raw_score / 10) * 100)

    if normalized >= 75:
        verdict = "apply"
    elif normalized >= 55:
        verdict = "maybe"
    else:
        verdict = "skip"

    return FinalDecision(
        match_score=normalized,
        verdict=verdict,
        missing_skills=missing_skills
    )
