from src.report_generator import generate_report

generate_report(
    ats_score=0.84,
    skill_score=1.0,
    semantic_score=0.73,
    matched_skills=[
        "python",
        "sql",
        "docker"
    ],
    missing_skills=[
        "aws",
        "kubernetes"
    ]
)

print("PDF generated!")