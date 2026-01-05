from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
You are a senior ATS parser and recruitment analyst.

Your task is to extract structured, normalized information from the Job Description below.

RULES:
- Use only information explicitly stated or strongly implied in the JD.
- Do NOT hallucinate skills or tools.
- Normalize skill and tool names (e.g., "Python programming" → "Python").
- Group similar skills together.
- If information is missing, return an empty list or null.
- Output MUST be valid JSON and NOTHING ELSE.

Return JSON with EXACTLY these keys:
{
  "role": string | null,
  "required_skills": [string],
  "nice_to_have_skills": [string],
  "experience_years": string | null,
  "tools_technologies": [string]
}

Job Description:
{jd_text}
""",
    input_variables=["jd_text"]
)


def extract_jd_structure(jd_text: str):
    chain = prompt | llm | parser
    return chain.invoke({"jd_text": jd_text})

