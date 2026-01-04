import requests
from bs4 import BeautifulSoup
from pathlib import Path
from utils.resume_loader import load_resume

HEADERS = {"User-Agent": "Mozilla/5.0"}

def load_jd(jd_url=None, jd_file=None, jd_text=None):
    if jd_url:
        html = requests.get(jd_url, headers=HEADERS, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return clean_text(soup.get_text())

    if jd_file:
        return clean_text(load_resume(jd_file))

    if jd_text:
        return clean_text(jd_text)

    raise ValueError("No JD input provided")


def clean_text(text: str) -> str:
    return " ".join(text.split())

