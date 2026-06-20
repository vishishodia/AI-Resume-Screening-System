def calculate_skill_score(jd_skills, resume_skills):

    matched = set(jd_skills).intersection(set(resume_skills))
    score = len(matched) / len(jd_skills)

    return round(score,4)

def calculate_ats_score(skill_score, semantic_score):

    ats_score = (0.4 * skill_score + 0.6 * semantic_score)

    return round(ats_score, 4)