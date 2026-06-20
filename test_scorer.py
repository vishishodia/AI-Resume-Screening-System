from src.scorer import calculate_skill_score, calculate_ats_score

jd_skills = [
    "python",
    "sql",
    "tensorflow",
    "nlp"
]

resume_skills = [
    "python",
    "sql",
    "tensorflow"
]

skill_score = calculate_skill_score(
    jd_skills,
    resume_skills
)

semantic_score = 0.7966

ats_score = calculate_ats_score(
    skill_score,
    semantic_score
)

print(f"Skill Score: {skill_score*100:.2f}%")
print(f"Semantic Score: {semantic_score*100:.2f}%")
print(f"ATS Score: {ats_score*100:.2f}%")