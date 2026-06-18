from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-miniLM-L6-v2")

job_description = "Looking for a Machine Learning Engineer with Python,TensorFlow and Deep Learning experience."

resume = "Python Developer with experience in Deep Learning,TensorFlow and Machine Learning projects."

jd_embedding = model.encode(job_description)
resume_embedding = model.encode(resume)

score = cosine_similarity(
    [jd_embedding],
    [resume_embedding]
)[0][0]

print(f"similarity: {score:.4f}")