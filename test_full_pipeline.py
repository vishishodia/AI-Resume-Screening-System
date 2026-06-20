from src.parser import extract_text_from_pdf
from src.skills import extract_skills
from src.matcher import calculate_similarity
from src.scorer import calculate_skill_score, calculate_ats_score

job_description = """
Looking for an AI/ML Intern.

Required Skills:
Python
Machine Learning
SQL
Docker
FastAPI
PyTorch
"""
resume_text = extract_text_from_pdf("data/resumes/resume1.pdf")

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

print("\nResume Skills:")
print(resume_skills)

print("\nJD Skills:")
print(jd_skills)

print(f"\nSkill Score: {skill_score:.2f}")
print(f"Semantic Score: {semantic_score:.2f}")
print(f"ATS Score: {ats_score:.2f}")

