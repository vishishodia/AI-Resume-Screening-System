import os
from src.skills import extract_skills

for file in os.listdir("data/resumes"):
    path = f"data/resumes/{file}"

    with open(path) as f:
        text = f.read()

    print(f"\n{file}")
    print(extract_skills(text))


