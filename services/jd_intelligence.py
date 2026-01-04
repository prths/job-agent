from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
You are an ATS system.
Extract structured information from the Job Description below.

Return JSON with:
- role
- required_skills
- nice_to_have_skills
- experience_years
- tools_technologies

JD:
{jd_text}
""",
    input_variables=["jd_text"]
)

def extract_jd_structure(jd_text: str):
    chain = prompt | llm | parser
    return chain.invoke({"jd_text": jd_text})

