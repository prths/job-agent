from langchain_google_genai import ChatGoogleGenerativeAI
from app.utils.retries import retry_llm

@retry_llm()
def get_gemini(model_name: str):
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.2
    )
