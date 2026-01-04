from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2)

prompt = PromptTemplate(
    template="""
You are an expert recruiter.

Job Description:
{jd}

Resume:
{resume}

Explain:
1. Why this resume matches the JD
2. Strengths
3. Missing skills
4. Overall fit score (0-100)
""",
    input_variables=["jd", "resume"]
)

def explain_match(jd_text: str, resume_text: str) -> str:
    return llm.invoke(prompt.format(jd=jd_text, resume=resume_text)).content
