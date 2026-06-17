from src.skills import extract_skills

with open("data/resumes/resume1.txt", "r") as f:
    text = f.read()

skills = extract_skills(text)

print(skills)