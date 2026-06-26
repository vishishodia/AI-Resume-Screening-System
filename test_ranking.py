from src.ranker import rank_candidates

results = [
    {
        "name": "Resume_A.pdf",
        "ats_score": 0.81
    },
    {
        "name": "Resume_B.pdf",
        "ats_score": 0.64
    },
    {
        "name": "Resume_C.pdf",
        "ats_score": 0.92
    },
    {
        "name": "Resume_D.pdf",
        "ats_score": 0.74
    }
]

ranked = rank_candidates(results)

for index, candidate in enumerate(ranked, start=1):
    print(
        f"{index}. {candidate['name']} - {candidate['ats_score']:.2f}"
    )