import re

SKILLS = [
    "python",
    "machine learning",
    "deep learning",
    "tensorflow",
    "sql",
    "nlp",
    "java",
    "docker",
    "mysql"
]

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]',' ', text)
    return text

def extract_skills(text):
    text = preprocess_text(text)

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return sorted(list(set(found_skills)))