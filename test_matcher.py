from src.matcher import calculate_similarity

job_description = """
Looking for a Machine Learning Engineer with Python,
TensorFlow and Deep Learning experience.
"""

resume = """
Python Developer with experience in Deep Learning,
TensorFlow and Machine Learning projects.
"""


score = calculate_similarity(job_description, resume)

print(f"match score: {score}")