from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    ats_score,
    skill_score,
    semantic_score,
    matched_skills,
    missing_skills,
    output_path="ats_report.pdf"
):

    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Screening Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"ATS Score: {ats_score*100:.1f}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Skill Match: {skill_score*100:.1f}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Semantic Match: {semantic_score*100:.1f}%",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Matched Skills",
            styles["Heading2"]
        )
    )

    for skill in matched_skills:
        content.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "Missing Skills",
            styles["Heading2"]
        )
    )

    for skill in missing_skills:
        content.append(
            Paragraph(
                f"• {skill}",
                styles["Normal"]
            )
        )

    doc.build(content)

    return output_path