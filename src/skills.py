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

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills