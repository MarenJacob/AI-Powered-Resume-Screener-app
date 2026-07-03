from database.db import db


class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    candidate_name = db.Column(
        db.String(150)
    )

    email = db.Column(
        db.String(150)
    )

    skills = db.Column(
        db.Text
    )

    experience = db.Column(
        db.Text
    )

    resume_file = db.Column(
        db.String(300)
    )

    ai_score = db.Column(
        db.Float
    )

    matched_skills = db.Column(
        db.Text
    )

    missing_skills = db.Column(
        db.Text
    )

    recommendation = db.Column(
        db.Text
    )

    ai_generated_probability = db.Column(
        db.Float
    )

    # ====================================
    # COMPANY OWNERSHIP
    # ====================================

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id")
    )