from utils.jd_loader import load_jd
from utils.resume_loader import load_resume
from services.embedding_matcher import SemanticMatcher

# -------- INPUTS --------
JD_URL = input("Enter JD URL (or press Enter to skip): ").strip() or None
JD_FILE = None
JD_TEXT = None

resume_paths = [p.strip() for p in input(
    "Enter resume paths or URLs (comma separated): "
).split(",") if p.strip()]

# -------- LOAD JD --------
jd_text = load_jd(jd_url=JD_URL, jd_file=JD_FILE, jd_text=JD_TEXT)

# -------- LOAD RESUMES --------
resumes = {}
for path in resume_paths:
    path = path.strip()
    resumes[path] = load_resume(path)

# -------- MATCH --------
matcher = SemanticMatcher()
ranking = matcher.rank_resumes(jd_text, resumes)

print("\n📊 Resume Ranking:")
for name, score in ranking:
    print(f"{name}  -->  {score}")

print(f"\n🏆 Best Resume: {ranking[0][0]}")

