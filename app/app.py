import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.parser import extract_text_from_pdf
from src.skills import extract_skills
from src.matcher import calculate_similarity
from src.scorer import calculate_skill_score, calculate_ats_score


st.title("AI Resume Screening System")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

if uploaded_file:
    st.success("Resume uploaded successfully!")

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload a resume.")
    
    elif not job_description.strip():
        st.error("Please enter a Job Description.")

    else:

        pdf_path = os.path.join(
            "temp",
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("Resume uploaded.")

        resume_text = extract_text_from_pdf(
            pdf_path
        )

        st.write("Resume text extracted.")

        resume_skills = extract_skills(
            resume_text
        )

        jd_skills = extract_skills(
            job_description
        )

        st.subheader("Resume Skills")
        st.write(resume_skills)

        st.subheader("JD Skills")
        st.write(jd_skills)

        semantic_score = calculate_similarity(
            resume_text,
            job_description
        )

        skill_score = calculate_skill_score(
            jd_skills,
            resume_skills
        )

        ats_score = calculate_ats_score(
            skill_score,
            semantic_score
        )

        st.subheader("Results")

        st.write(
            f"Skill Score: {skill_score:.2f}"
        )

        st.write(
            f"Semantic Score: {semantic_score:.2f}"
        )

        st.write(
            f"ATS Score: {ats_score * 100:.1f}%"
        )

        matched_skills = list(
            set(jd_skills).intersection(
                set(resume_skills)
            )
        )

        st.subheader("Matched Skills")
        st.write(matched_skills)

        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        st.subheader("Missing Skills")
        st.write(missing_skills)