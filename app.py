import streamlit as st
import tempfile

from utils.jd_loader import load_jd
from utils.resume_loader import load_resume
from services.embedding_matcher import SemanticMatcher
from services.cover_letter import generate_cover_letter
from services.llm_matcher import llm_match
from services.score_fusion import fuse_scores

st.set_page_config(page_title="Job Application Agent", layout="centered")
st.title("🧠 AI Job Application Agent")

# ---------------- JD INPUT ----------------
st.header("📄 Job Description")
jd_url = st.text_input("JD URL (LinkedIn / Career page)")
jd_text = st.text_area("Or paste JD text here", height=200)

# ---------------- RESUME INPUT ----------------
st.header("📎 Upload Resume(s)")
uploaded_files = st.file_uploader(
    "Upload one or more resumes (PDF / DOCX / TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# ---------------- RUN MATCHING ----------------
if st.button("🔍 Run Matching"):
    if not (jd_url or jd_text):
        st.error("Please provide a JD URL or JD text.")
        st.stop()

    if not uploaded_files:
        st.error("Please upload at least one resume.")
        st.stop()

    # ---- Load JD ----
    with st.spinner("Loading job description..."):
        jd_content = load_jd(
            jd_url=jd_url if jd_url else None,
            jd_text=jd_text if jd_text else None
        )

    # ---- Load resumes ----
    resumes = {}
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as tmp:
            tmp.write(file.read())
            resumes[file.name] = load_resume(tmp.name)

    # ---- Semantic matching ----
    with st.spinner("Running semantic matching..."):
        matcher = SemanticMatcher()
        ranking = matcher.rank_resumes(jd_content, resumes)

    st.success("Matching complete!")

    # ---------------- RESULTS ----------------
    st.subheader("📊 Resume Ranking")
    for name, score in ranking:
        st.write(f"**{name}** → {score:.3f}")

    best_resume_name = ranking[0][0]
    best_resume_text = resumes[best_resume_name]

    st.subheader("🏆 Best Resume")
    st.write(f"**{best_resume_name}**")

# ---------------- LLM ANALYSIS ----------------
if st.button("🤖 Analyze Best Resume"):
with st.spinner("Running LLM evaluation..."):
    llm_result = llm_match(jd_content, best_resume_text)

st.subheader("🧠 LLM Match Analysis")
st.json(llm_result)

# ---------- HYBRID SCORE ----------
embedding_score = ranking[0][1]        # 0–1
llm_score = llm_result["fit_score"]    # 0–100

final_score = fuse_scores(embedding_score, llm_score)

st.subheader("📈 Final Hybrid Score")
st.metric("Overall Fit", f"{final_score}/100")

# ---------- SKILL GAP ----------
st.subheader("🧩 Skill Gap Analysis")
missing_skills = llm_result.get("missing_skills", [])

if missing_skills:
    st.warning("Skills / areas to improve:")
    for skill in missing_skills:
        st.write(f"• {skill}")
else:
    st.success("No major skill gaps identified 🎯")

# ---------- COVER LETTER ----------
if st.button("✉️ Generate Cover Letter"):
    with st.spinner("Generating cover letter..."):
        cover_letter = generate_cover_letter(
            jd_content,
            best_resume_text,
            llm_result
        )

    st.text_area(
        "Generated Cover Letter",
        cover_letter,
        height=350
    )
