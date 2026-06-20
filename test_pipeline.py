from src.parser import extract_text_from_pdf
from src.skills import extract_skills

text = extract_text_from_pdf("data/resumes/resume1.pdf")

skills = extract_skills(text)

print("\nDetected skills")
print(skills)