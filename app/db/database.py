import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "job_agent.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resume_hash TEXT NOT NULL,
        job_hash TEXT NOT NULL,
        match_score INTEGER,
        verdict TEXT,
        cover_letter TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(resume_hash, job_hash)
    )
    """)

    conn.commit()
    conn.close()
