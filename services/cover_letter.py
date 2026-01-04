from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.4
)

prompt = PromptTemplate(
    template="""
You are a professional career coach.

Write a concise, ATS-friendly cover letter using the information below.

Job Description:
{jd}

Candidate Resume:
{resume}

Match Summary:
- Fit score: {fit_score}/100
- Strengths: {strengths}
- Missing skills (do NOT mention directly): {missing_skills}

Guidelines:
- 250–300 words
- Professional, confident tone
- Focus on strengths aligned with JD
- Do NOT mention weaknesses explicitly
""",
    input_variables=[
        "jd", "resume", "fit_score", "strengths", "missing_skills"
    ]
)

def generate_cover_letter(jd, resume, llm_result):
    return llm.invoke(
        prompt.format(
            jd=jd,
            resume=resume,
            fit_score=llm_result["fit_score"],
            strengths=", ".join(llm_result["strengths"]),
            missing_skills=", ".join(llm_result["missing_skills"])
        )
    ).content

