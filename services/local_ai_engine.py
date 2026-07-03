import re

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# DETECT SKILLS
# ==========================================

SKILLS_DATABASE = [

    "python",
    "flask",
    "django",
    "javascript",
    "react",
    "nodejs",
    "sql",
    "mysql",
    "photoshop",
    "illustrator",
    "figma",
    "ui",
    "ux",
    "graphic design",
    "branding",
    "video editing",
    "machine learning",
    "data analysis",
    "communication",
    "leadership",
    "marketing",
    "seo"
]

# ==========================================
# CLEAN TEXT
# ==========================================

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    return text

# ==========================================
# SEMANTIC SCORE
# ==========================================

def semantic_similarity(resume, job_description):

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform([

        resume,

        job_description
    ])

    similarity = cosine_similarity(

        vectors[0:1],

        vectors[1:2]
    )

    return round(
        float(similarity[0][0]) * 100,
        2
    )

# ==========================================
# DETECT SKILLS
# ==========================================

def detect_skills(text):

    text = clean_text(text)

    detected = []

    for skill in SKILLS_DATABASE:

        if skill.lower() in text:

            detected.append(skill)

    return detected

# ==========================================
# MATCH SKILLS
# ==========================================

def skill_matching(

    resume_skills,

    job_description
):

    matched = []

    missing = []

    job_description = clean_text(
        job_description
    )

    for skill in SKILLS_DATABASE:

        if skill in job_description:

            if skill in resume_skills:

                matched.append(skill)

            else:

                missing.append(skill)

    return matched, missing

# ==========================================
# EXPERIENCE DETECTION
# ==========================================

def detect_experience(resume_text):

    patterns = [

        r'(\d+)\+?\s+years',

        r'(\d+)\+?\s+yrs'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            resume_text.lower()
        )

        if match:

            return int(match.group(1))

    return 0

# ==========================================
# FINAL AI ANALYSIS
# ==========================================

def analyze_candidate(

    resume_text,

    job_description
):

    semantic_score = semantic_similarity(

        resume_text,

        job_description
    )

    detected_skills = detect_skills(
        resume_text
    )

    matched_skills, missing_skills = skill_matching(

        detected_skills,

        job_description
    )

    experience_years = detect_experience(
        resume_text
    )

    skill_score = 0

    if len(matched_skills) > 0:

        total_required = (

            len(matched_skills)

            + len(missing_skills)
        )

        skill_score = round(

            (len(matched_skills) / total_required)

            * 100,

            2
        )

    final_score = round(

        (semantic_score * 0.6)

        + (skill_score * 0.4),

        2
    )

    # ======================================
    # RECOMMENDATION
    # ======================================

    if final_score >= 80:

        recommendation = "Highly Recommended"

    elif final_score >= 60:

        recommendation = "Recommended"

    elif final_score >= 40:

        recommendation = "Average Match"

    else:

        recommendation = "Low Match"

    return {

        "final_score": final_score,

        "semantic_score": semantic_score,

        "skill_score": skill_score,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "detected_skills": detected_skills,

        "experience_years": experience_years,

        "recommendation": recommendation,

        "ai_generated_probability": round(

            100 - semantic_score,

            2
        )
    }