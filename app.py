import streamlit as st
from resume_parser import extract_text
from scorer import get_score

st.set_page_config(page_title="TalentFlow AI", layout="wide")

st.title("🚀 TalentFlow AI Resume Screener")

job_description = st.text_area("📄 Enter Job Description")

uploaded_files = st.file_uploader(
    "📂 Upload Resumes",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("🔍 Analyze Candidates"):
    results = []

    for file in uploaded_files:
        text = extract_text(file)
        score = get_score(text, job_description)

        results.append({
            "name": file.name,
            "score": score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.subheader("🏆 Ranked Candidates")

    for r in results:
        st.progress(int(r["score"]))
        st.write(f"**{r['name']}** — {r['score']}%")
