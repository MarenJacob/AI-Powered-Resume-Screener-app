import fitz

import docx

import re

# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_text_from_pdf(file_path):

    text = ""

    try:

        document = fitz.open(file_path)

        for page in document:

            text += page.get_text()

    except Exception as e:

        print("PDF EXTRACTION ERROR")

        print(str(e))

    return text

# ==========================================
# DOCX TEXT EXTRACTION
# ==========================================

def extract_text_from_docx(file_path):

    text = ""

    try:

        document = docx.Document(file_path)

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

    except Exception as e:

        print("DOCX EXTRACTION ERROR")

        print(str(e))

    return text

# ==========================================
# DETECT FILE TYPE
# ==========================================

def extract_resume_text(file_path):

    if file_path.endswith(".pdf"):

        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):

        return extract_text_from_docx(file_path)

    else:

        return ""

# ==========================================
# EXTRACT EMAIL
# ==========================================

def extract_email(text):

    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    matches = re.findall(pattern, text)

    if matches:

        return matches[0]

    return "Not Found"

# ==========================================
# EXTRACT PHONE NUMBER
# ==========================================

def extract_phone(text):

    pattern = r"(\+?\d[\d\s\-\(\)]{7,}\d)"

    matches = re.findall(pattern, text)

    if matches:

        return matches[0]

    return "Not Found"

# ==========================================
# EXTRACT SKILLS
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
    "graphic design",
    "branding",
    "ui",
    "ux",
    "seo",
    "marketing",
    "leadership",
    "communication",
    "video editing",
    "machine learning",
    "data analysis"
]

def extract_skills(text):

    detected_skills = []

    text = text.lower()

    for skill in SKILLS_DATABASE:

        if skill.lower() in text:

            detected_skills.append(skill)

    return detected_skills

# ==========================================
# MAIN RESUME EXTRACTION
# ==========================================

def extract_resume_data(file_path):

    raw_text = extract_resume_text(file_path)

    email = extract_email(raw_text)

    phone = extract_phone(raw_text)

    skills = extract_skills(raw_text)

    return {

        "raw_text": raw_text,

        "email": email,

        "phone": phone,

        "skills": skills
    }