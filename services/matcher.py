def compute_match_score(jd_text: str, resume_text: str) -> float:
    jd_words = set(jd_text.lower().split())
    resume_words = set(resume_text.lower().split())

    if not jd_words:
        return 0.0

    return round(len(jd_words & resume_words) / len(jd_words), 3)


def rank_resumes(jd_text: str, resumes: dict):
    """
    resumes = { "resume1.pdf": "text", "resume2.pdf": "text" }
    """
    scores = {}

    for name, text in resumes.items():
        scores[name] = compute_match_score(jd_text, text)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked

