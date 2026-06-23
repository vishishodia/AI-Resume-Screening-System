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

st.sidebar.title("About")

st.sidebar.info(
    """
    AI Resume Screening System

    Features:
    - Resume Parsing
    - Skill Extraction
    - Semantic Matching
    - ATS Scoring
    """
)

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

        st.subheader("Resume Statistics")

        st.metric(
            "Skills Detected",
            len(resume_skills)
        )

        jd_skills = extract_skills(
            job_description
        )
        if len(jd_skills) == 0:
            st.warning(
                "No known skills detected in the Job Description."
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

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "ATS Score",
                f"{ats_score * 100:.1f}%"
            )

        with col2:
            st.metric(
                "Skill Match",
                f"{skill_score * 100:.1f}%"
            )

        with col3:
            st.metric(
                "Semantic Match",
                f"{semantic_score * 100:.1f}%"
            )
        
        st.subheader("Overall Match")

        st.progress(
            int(ats_score * 100)
        )

        if ats_score >= 0.85:
            st.success("Excellent Match")

        elif ats_score >= 0.70:
            st.info("Good Match")

        elif ats_score >= 0.50:
            st.warning("Average Match")

        else:
            st.error("Poor Match")


        matched_skills = list(
            set(jd_skills).intersection(
                set(resume_skills)
            )
        )

        st.subheader("Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.success(f"✓ {skill}")
        else:
            st.info("No matching skills found.")

        missing_skills = list(
            set(jd_skills) - set(resume_skills)
        )

        st.subheader("Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.warning(f"✗ {skill}")
        else:
            st.success("No missing skills.")