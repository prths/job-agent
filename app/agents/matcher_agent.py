from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.utils.parsers import MatchResult
from app.llms.gemini import get_gemini
from app.utils.logger import get_logger

logger = get_logger("MatcherAgent")


def match_resume(resume: str, jd: str) -> MatchResult:
    parser = PydanticOutputParser(pydantic_object=MatchResult)

    prompt = PromptTemplate(
        template="""
You are a strict technical evaluator.

Evaluate how well the resume matches the job description.

Rules:
- Give a raw_score between 0 and 10
- 0 = no match
- 10 = perfect match
- Be conservative, do not inflate scores
- List important missing skills explicitly

{format_instructions}

Resume:
{resume}

Job Description:
{jd}
""",
        input_variables=["resume", "jd"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    llm = get_gemini("gemini-2.5-pro")
    chain = prompt | llm | parser

    result = chain.invoke({"resume": resume, "jd": jd})

    logger.info(f"Raw score from LLM: {result.raw_score}")
    return result
