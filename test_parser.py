from src.parser import extract_text_from_pdf

text = extract_text_from_pdf("data/resumes/resume1.pdf")

print(text)