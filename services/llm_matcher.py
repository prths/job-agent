from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0
)

prompt = PromptTemplate(
    template="""
You are a senior ATS evaluator.

Evaluate the resume against the job description.

Return STRICT JSON:
{{
  "fit_score": number (0-100),
  "strengths": [list],
  "missing_skills": [list],
  "experience_match": "poor | partial | strong",
  "decision": "reject | borderline | strong match"
}}

Job Description:
{jd}

Resume:
{resume}
""",
    input_variables=["jd", "resume"]
)

parser = JsonOutputParser()

def llm_match(jd_text: str, resume_text: str):
    chain = prompt | llm | parser
    return chain.invoke({"jd": jd_text, "resume": resume_text})

