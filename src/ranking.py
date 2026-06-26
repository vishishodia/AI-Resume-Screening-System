def rank_resumes(resume_scores):
    return sorted(
        resume_scores,
        key=lambda x: x[1],
        reverse=True
    )