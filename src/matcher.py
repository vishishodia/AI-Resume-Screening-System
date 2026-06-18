from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(job_description, resume_text):
    jd_embedding = model.encode(job_description)
    resume_embedding = model.encode(resume_text)

    score = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
    )[0][0]

    return round(float(score),4)
