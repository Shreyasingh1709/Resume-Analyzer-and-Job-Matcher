import streamlit as st
import requests
import io

st.set_page_config(page_title="Resume Analyzer & Job Matcher", layout="centered")
st.title("Resume Analyzer & Job Matcher")

st.markdown("""
Upload your resume (PDF/TXT) and job description (PDF/TXT).\
Get a match score, extracted skills, and suggestions to improve your resume!
""")



# Resume upload
resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"], key="resume")

# Job description upload or paste
st.markdown("**Job Description** (upload a file or paste below)")
job_file = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"], key="jobdesc")
job_description = st.text_area("Or paste Job Description", height=200)

analyze = st.button("Analyze & Match")

if analyze:
    if not resume_file or (not job_file and not job_description.strip()):
        st.warning("Please upload a resume and provide a job description (upload or paste).")
    else:
        files = {"resume": (resume_file.name, resume_file, resume_file.type)}
        data = {}
        if job_file:
            files["job_description_file"] = (job_file.name, job_file, job_file.type)
        elif job_description.strip():
            data["job_description"] = job_description
        try:
            response = requests.post(
                "http://localhost:8000/analyze_match", files=files, data=data if data else None, timeout=60
            )
            if response.status_code == 200:
                result = response.json()
                st.subheader("Match Score")
                st.metric("Score", f"{result.get('match_score', 0)}%")
                st.subheader("Extracted Skills & Experience")
                st.write(result.get("extracted_skills", "-"))
                st.subheader("Suggestions for Improvement")
                st.write(result.get("suggestions", "-"))
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
