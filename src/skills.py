import re

SKILLS = [

    # Programming
    "python",
    "java",
    "c++",
    "javascript",
    "sql",

    # Databases
    "mysql",
    "postgresql",
    "mongodb",

    # AI/ML
    "machine learning",
    "deep learning",
    "nlp",
    "rag",
    "tensorflow",
    "pytorch",
    "scikit-learn",

    # Data
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",

    # Backend
    "fastapi",
    "flask",
    "django",

    # DevOps
    "docker",
    "kubernetes",
    "jenkins",
    "terraform",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # Cybersecurity
    "network security",
    "ethical hacking",
    "penetration testing",
    "wireshark",
    "burp suite",
    "nmap",
    "metasploit",
    "kali linux",
    "siem",
    "incident response",
    "vulnerability assessment",
    "owasp",

    # Data Engineering
    "spark",
    "kafka",
    "airflow",
    "hadoop"
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