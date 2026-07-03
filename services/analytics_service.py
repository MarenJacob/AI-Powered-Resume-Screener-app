from models.resume_model import Resume

# ==========================================
# GENERATE ANALYTICS
# ==========================================
# `companies` is optional so this stays backward-compatible with
# auth_routes.py's dashboard(), which only ever has one company's
# resumes in scope and doesn't need a company count.

def generate_analytics(resumes, companies=None):

    # --------------------------------------
    # TOTAL CANDIDATES
    # --------------------------------------

    total_candidates = len(resumes)

    # --------------------------------------
    # AVERAGE AI SCORE
    # --------------------------------------

    average_score = 0

    if total_candidates > 0:

        total_score = sum([
            resume.ai_score or 0
            for resume in resumes
        ])

        average_score = round(
            total_score / total_candidates,
            2
        )

    # --------------------------------------
    # SHORTLISTED CANDIDATES
    # --------------------------------------

    shortlisted = len([

        resume for resume in resumes

        if resume.ai_score and resume.ai_score >= 70
    ])

    # --------------------------------------
    # LOW MATCH CANDIDATES
    # --------------------------------------

    low_matches = len([

        resume for resume in resumes

        if resume.ai_score and resume.ai_score < 50
    ])

    # --------------------------------------
    # TOTAL COMPANIES (admin-only metric)
    # --------------------------------------

    total_companies = len(companies) if companies is not None else 0

    # --------------------------------------
    # RETURN ANALYTICS DATA
    # --------------------------------------

    return {

        "total_candidates": total_candidates,

        "average_score": average_score,

        "shortlisted": shortlisted,

        "low_matches": low_matches,

        "total_companies": total_companies
    }
