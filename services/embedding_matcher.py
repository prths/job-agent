from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticMatcher:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.model.encode(texts, normalize_embeddings=True)

    def rank_resumes(self, jd_text: str, resumes: dict):
        """
        resumes = { "resume_name": "resume_text" }
        """
        resume_names = list(resumes.keys())
        resume_texts = list(resumes.values())

        resume_embeddings = self.embed(resume_texts)
        jd_embedding = self.embed([jd_text])

        dim = resume_embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(resume_embeddings)

        scores, indices = index.search(jd_embedding, k=len(resume_names))

        ranked = []
        for score, idx in zip(scores[0], indices[0]):
            ranked.append((resume_names[idx], round(float(score), 4)))

        return ranked
