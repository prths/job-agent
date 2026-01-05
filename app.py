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

    with st.spinner("Loading job description..."):
        st.session_state.jd_content = load_jd(
            jd_url=jd_url if jd_url else None,
            jd_text=jd_text if jd_text else None
        )

    resumes = {}
    for file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.name) as tmp:
            tmp.write(file.read())
            resumes[file.name] = load_resume(tmp.name)

    with st.spinner("Running semantic matching..."):
        matcher = SemanticMatcher()
        st.session_state.ranking = matcher.rank_resumes(
            st.session_state.jd_content,
            resumes
        )
        st.session_state.resumes = resumes

    st.success("Matching complete!")

# ---------------- SHOW MATCHING RESULTS ----------------
if "ranking" in st.session_state:
    st.subheader("📊 Resume Ranking")
    for name, score in st.session_state.ranking:
        st.write(f"**{name}** → {score:.3f}")

    best_resume_name = st.session_state.ranking[0][0]
    st.session_state.best_resume_text = st.session_state.resumes[best_resume_name]

    st.subheader("🏆 Best Resume")
    st.write(f"**{best_resume_name}**")

# ---------------- LLM ANALYSIS ----------------
if "best_resume_text" in st.session_state:
    if st.button("🤖 Analyze Best Resume"):
        with st.spinner("Running LLM evaluation..."):
            st.session_state.llm_result = llm_match(
                st.session_state.jd_content,
                st.session_state.best_resume_text
            )

# ---------------- SHOW LLM RESULTS ----------------
if "llm_result" in st.session_state:
    llm_result = st.session_state.llm_result

    st.subheader("🧠 LLM Match Analysis")
    st.json(llm_result)

    embedding_score = st.session_state.ranking[0][1]
    llm_score = llm_result["fit_score"]

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

# ---------------- COVER LETTER ----------------
if "llm_result" in st.session_state:
    if st.button("✉️ Generate Cover Letter"):
        with st.spinner("Generating cover letter..."):
            cover_letter = generate_cover_letter(
                st.session_state.jd_content,
                st.session_state.best_resume_text,
                st.session_state.llm_result
            )

        st.text_area(
            "Generated Cover Letter",
            cover_letter,
            height=350
        )
