from langchain_core.prompts import PromptTemplate
from app.llms.gemini import get_gemini
from app.utils.logger import get_logger

logger = get_logger("CoverAgent")


def generate_cover(resume: str, jd: str) -> str:
    logger.info("Generating cover letter")

    prompt = PromptTemplate(
        template="""
        Write a concise, professional cover letter.

        Resume:
        {resume}

        Job Description:
        {jd}
        """,
        input_variables=["resume", "jd"],
    )

    llm = get_gemini("gemini-2.5-pro")
    chain = prompt | llm

    return chain.invoke({"resume": resume, "jd": jd}).content
