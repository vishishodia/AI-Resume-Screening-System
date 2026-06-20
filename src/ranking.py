def rank_candidates(candidates):

    ranked = sorted(
        candidates,
        key=lambda x : x['ats_score'],
        reverse=True
    )

    return ranked