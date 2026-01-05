from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)

prompt = PromptTemplate(
    input_variables=["jd", "resume"],
    template="""
You are a **senior technical recruiter and ATS evaluator**.

Your task is to evaluate the resume against the job description using hiring best practices.

### Instructions
- Base your judgment strictly on evidence from the resume.
- Do NOT assume skills unless explicitly mentioned.
- Use concise, recruiter-style language.
- Be objective and ATS-oriented.
- Return **valid JSON only** (no markdown, no explanation outside JSON).

### Output JSON Schema
{
  "match_explanation": string,
  "strengths": [string],
  "missing_skills": [string],
  "concerns_or_gaps": [string],
  "overall_fit_score": number
}

### Scoring Rules
- 90–100: Excellent match (ready to hire)
- 75–89: Strong match (minor gaps)
- 60–74: Partial match (trainable)
- <60: Weak match

### Job Description
{jd}

### Resume
{resume}
"""
)

def explain_match(jd_text: str, resume_text: str) -> str:
    return llm.invoke(prompt.format(jd=jd_text, resume=resume_text)).content
