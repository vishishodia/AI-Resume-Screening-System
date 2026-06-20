from src.ranking import rank_candidates

candidates = [

    {
        "name": "Resume A",
        "ats_score": 0.778
    },

    {
        "name": "Resume B",
        "ats_score": 0.652
    },

    {
        "name": "Resume C",
        "ats_score": 0.914
    },

    {
        "name": "Resume D",
        "ats_score": 0.821
    },
    
    {
    "name": "Resume E",
    "ats_score": 0.95
}

]

ranked = rank_candidates(candidates)

for i, candidate in enumerate(ranked, start=1):
    print(
        f"{i},"
        f"{candidate['name']}"
        f"-{candidate['ats_score']*100:.2f}"
    )