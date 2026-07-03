from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import current_user

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from services.recommendation_service import generate_recommendation

import os

from database.db import db

from models.resume_model import Resume

from services.parser_services import extract_resume_data

from services.colab_ai_service import analyze_resume_with_ai

resume = Blueprint('resume', __name__)

UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# UPLOAD RESUME
# ==========================================

@resume.route("/upload-resume", methods=["GET", "POST"])
@login_required
def upload_resume():

    if request.method == "POST":

        candidate_name = request.form.get("candidate_name")
        job_description = request.form.get("job_description")

        file = request.files.get("resume")

        if not file:
            flash("Please select a resume file", "error")
            return redirect(url_for("resume.upload_resume"))

        allowed_extensions = [".pdf", ".docx"]

        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        if file_extension not in allowed_extensions:

            flash(
                "Only PDF and DOCX files are allowed",
                "error"
            )

            return redirect(
                url_for("resume.upload_resume")
            )

        filename = secure_filename(file.filename)

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(filepath)

        try:

            extracted_data = extract_resume_data(
                filepath
            )

            ai_results = analyze_resume_with_ai(

                extracted_data["raw_text"],

                job_description
            )

        except Exception as e:

            print("AI ERROR:", e)

            flash(
                "AI Server unavailable",
                "error"
            )

            return render_template(
                "resumes/upload_resume.html"
            )

        local_recommendation = generate_recommendation(

            ai_results["final_score"]
        )

        candidate = Resume(

            candidate_name=candidate_name,

            email=extracted_data.get(
                "email",
                "Not Found"
            ),

            skills=", ".join(
                ai_results["detected_skills"]
            ),

            experience=extracted_data[
                "raw_text"
            ],

            resume_file=filename,

            ai_score=ai_results[
                "final_score"
            ],

            matched_skills=", ".join(
                ai_results["matched_skills"]
            ),

            missing_skills=", ".join(
                ai_results["missing_skills"]
            ),

            recommendation=
                local_recommendation["decision"],

            ai_generated_probability=
                ai_results[
                    "ai_generated_probability"
                ],

            company_id=
                current_user.company_id
        )

        db.session.add(candidate)

        db.session.commit()

        flash(
            "Candidate analyzed successfully",
            "success"
        )

        return redirect(
            url_for("resume.candidates")
        )

    return render_template(
        "resumes/upload_resume.html"
    )
# ==========================================
# VIEW CANDIDATES
# ==========================================

@resume.route("/candidates")
@login_required
def candidates():

    candidates = Resume.query.filter_by(
    company_id=current_user.company_id
    ).order_by(
        Resume.ai_score.desc()
    ).all()

    return render_template(
        "resumes/candidates.html",
        candidates=candidates
    )