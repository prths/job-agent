import pdfplumber
import fitz
import requests
import tempfile
from docx import Document
from pathlib import Path
from urllib.parse import urlparse


def is_url(path: str) -> bool:
    return path.startswith("http://") or path.startswith("https://")


def download_file(url: str) -> str:
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    suffix = Path(urlparse(url).path).suffix or ".pdf"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    tmp.write(response.content)
    tmp.close()

    return tmp.name


def load_resume(file_path: str) -> str:
    if is_url(file_path):
        file_path = download_file(file_path)

    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    if ext == ".docx":
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)

    if ext == ".txt":
        return Path(file_path).read_text()

    raise ValueError(f"Unsupported resume format: {ext}")

