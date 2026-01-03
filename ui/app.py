import streamlit as st
import requests

st.set_page_config(
    page_title="Job Application Agent",
    layout="wide"
)

st.title("🤖 Job Application Agent")

st.markdown(
    """
Paste your **resume** and **job description** below.
The system will evaluate the match and generate a cover letter if applicable.
"""
)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    api_url = st.text_input(
        "FastAPI URL",
        value="http://localhost:8000"
    )

# Input columns
col1, col2 = st.columns(2)

with col1:
    resume = st.text_area(
        "📄 Resume",
        height=300,
        placeholder="Paste resume text here..."
    )

with col2:
    job_description = st.text_area(
        "🧾 Job Description",
        height=300,
        placeholder="Paste job description here..."
    )

# Submit
if st.button("🚀 Evaluate & Apply"):
    if not resume.strip() or not job_description.strip():
        st.error("Please provide both resume and job description.")
    else:
        with st.spinner("Evaluating..."):
            try:
                response = requests.post(
                    f"{api_url}/apply",
                    json={
                        "resume": resume,
                        "job_description": job_description
                    },
                    timeout=120
                )

                if response.status_code != 200:
                    st.error("API error")
                    st.code(response.text)
                else:
                    result = response.json()

                    st.success("Evaluation complete")

                    st.metric(
                        "Match Score",
                        f"{result['match_score']} / 100"
                    )

                    verdict = result["verdict"]

                    if verdict == "apply":
                        st.success("✅ Recommended: APPLY")
                    elif verdict == "maybe":
                        st.warning("⚠️ Recommended: MAYBE")
                    else:
                        st.error("❌ Recommended: SKIP")

                    if result.get("cover_letter"):
                        st.subheader("✉️ Generated Cover Letter")
                        st.text_area(
                            "",
                            value=result["cover_letter"],
                            height=350
                        )

            except Exception as e:
                st.error("Request failed")
                st.exception(e)
