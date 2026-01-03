from app.utils.logger import get_logger

logger = get_logger("ResumeAgent")

def parse_resume(resume_text: str) -> str:
    logger.info("Parsing resume")
    return resume_text.strip()
