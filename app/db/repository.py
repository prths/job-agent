from app.db.database import get_connection
from app.utils.hash import hash_text


def find_application(resume: str, job_description: str):
    conn = get_connection()
    cur = conn.cursor()

    resume_hash = hash_text(resume)
    job_hash = hash_text(job_description)

    cur.execute(
        "SELECT * FROM applications WHERE resume_hash=? AND job_hash=?",
        (resume_hash, job_hash),
    )

    row = cur.fetchone()
    conn.close()
    return row


def save_application(
    resume: str,
    job_description: str,
    match_score: int,
    verdict: str,
    cover_letter: str,
):
    conn = get_connection()
    cur = conn.cursor()

    resume_hash = hash_text(resume)
    job_hash = hash_text(job_description)

    cur.execute(
        """
        INSERT OR IGNORE INTO applications
        (resume_hash, job_hash, match_score, verdict, cover_letter)
        VALUES (?, ?, ?, ?, ?)
        """,
        (resume_hash, job_hash, match_score, verdict, cover_letter),
    )

    conn.commit()
    conn.close()
