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
from src.report_generator import generate_report
from src.ranking import rank_resumes

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Screening System")

st.sidebar.title("About")

st.sidebar.info("""
AI Resume Screening System

Features

• Resume Parsing
• Skill Extraction
• Semantic Matching
• ATS Scoring
• PDF Report
• Resume Ranking
""")

uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area(
    "Paste Job Description",
    height=220
)

if st.button("Analyze Resumes"):

    if not uploaded_files:
        st.error("Please upload at least one resume.")

    elif not job_description.strip():
        st.error("Please paste a Job Description.")

    else:

        os.makedirs("temp", exist_ok=True)

        ranking_data = []

        for i, uploaded_file in enumerate(uploaded_files):

            pdf_path = os.path.join(
                "temp",
                uploaded_file.name
            )

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            resume_text = extract_text_from_pdf(pdf_path)

            resume_skills = extract_skills(resume_text)

            jd_skills = extract_skills(job_description)

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

            ranking_data.append(
                (
                    uploaded_file.name,
                    ats_score
                )
            )

            st.divider()

            st.header(uploaded_file.name)

            st.metric(
                "ATS Score",
                f"{ats_score*100:.1f}%"
            )

            st.progress(
                int(ats_score*100)
            )

            if ats_score >= 0.85:
                st.success("Excellent Match")

            elif ats_score >= 0.70:
                st.info("Good Match")

            elif ats_score >= 0.50:
                st.warning("Average Match")

            else:
                st.error("Poor Match")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Skill Match",
                    f"{skill_score*100:.1f}%"
                )

            with col2:
                st.metric(
                    "Semantic Match",
                    f"{semantic_score*100:.1f}%"
                )

            with col3:
                st.metric(
                    "Skills Detected",
                    len(resume_skills)
                )

            st.subheader("Matched Skills")

            matched = list(
                set(jd_skills).intersection(
                    set(resume_skills)
                )
            )

            if matched:

                for skill in matched:
                    st.success(f"✓ {skill}")

            else:
                st.info("No matching skills.")

            st.subheader("Missing Skills")

            missing = list(
                set(jd_skills) - set(resume_skills)
            )

            if missing:

                for skill in missing:
                    st.warning(f"✗ {skill}")

            else:
                st.success("No missing skills.")

            report_file = generate_report(
                ats_score,
                skill_score,
                semantic_score,
                matched,
                missing
            )

            with open(report_file, "rb") as pdf:
                st.download_button(
                    label="📄 Download ATS Report",
                    data=pdf,
                    file_name=report_file,
                    mime="application/pdf",
                    key=f"download_{i}"
                )

        st.divider()

        st.header("🏆 Resume Ranking")

        ranked = rank_resumes(ranking_data)

        for i, (name, score) in enumerate(ranked, start=1):

            st.write(
                f"**{i}. {name}** — {score*100:.1f}%"
            )