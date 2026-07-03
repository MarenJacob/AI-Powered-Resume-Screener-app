def compare_candidates(candidates):

    """
    Compare multiple candidates
    based on AI scores and skills.
    """

    if not candidates:

        return {

            "best_candidate": None,

            "worst_candidate": None,

            "average_score": 0,

            "total_candidates": 0,

            "skill_diversity": 0
        }

    # --------------------------------------
    # SORT CANDIDATES BY SCORE
    # --------------------------------------

    sorted_candidates = sorted(

        candidates,

        key=lambda x: x.get("score", 0),

        reverse=True
    )

    # --------------------------------------
    # BEST + WORST
    # --------------------------------------

    best_candidate = sorted_candidates[0]

    worst_candidate = sorted_candidates[-1]

    # --------------------------------------
    # AVERAGE SCORE
    # --------------------------------------

    scores = [

        c.get("score", 0)

        for c in candidates
    ]

    average_score = round(

        sum(scores) / len(scores),

        2
    )

    # --------------------------------------
    # SKILL DIVERSITY
    # --------------------------------------

    all_skills = set()

    for candidate in candidates:

        skills = candidate.get("skills", [])

        if isinstance(skills, str):

            skills = skills.split(",")

        for skill in skills:

            cleaned = skill.strip()

            if cleaned:

                all_skills.add(cleaned)

    # --------------------------------------
    # RETURN RESULTS
    # --------------------------------------

    return {

        "best_candidate": best_candidate,

        "worst_candidate": worst_candidate,

        "average_score": average_score,

        "total_candidates": len(candidates),

        "skill_diversity": len(all_skills)
    }