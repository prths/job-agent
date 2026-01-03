from fastapi import APIRouter, HTTPException
from app.api.schemas import ApplyRequest, ApplyResponse
from app.main import run_pipeline
from app.db.repository import find_application, save_application
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger("API")


@router.post("/apply", response_model=ApplyResponse)
def apply_job(request: ApplyRequest):
    logger.info("Received /apply request")

    existing = find_application(
        request.resume,
        request.job_description
    )

    if existing:
        logger.info("Duplicate application detected")
        return ApplyResponse(
            match_score=existing["match_score"],
            verdict=existing["verdict"],
            cover_letter=existing["cover_letter"],
        )

    result = run_pipeline(
        resume=request.resume,
        job_description=request.job_description
    )

    save_application(
        resume=request.resume,
        job_description=request.job_description,
        match_score=result["match_score"],
        verdict=result["verdict"],
        cover_letter=result["cover_letter"],
    )

    return ApplyResponse(
        match_score=result["match_score"],
        verdict=result["verdict"],
        cover_letter=result["cover_letter"],
    )
