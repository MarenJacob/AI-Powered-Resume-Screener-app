from flask import Blueprint
from flask import render_template

from flask_login import login_required
from flask_login import current_user

from models.resume_model import Resume
from models.user_model import User
from models.company_model import Company

from services.analytics_service import generate_analytics

# ==========================================
# ADMIN BLUEPRINT
# ==========================================

admin = Blueprint(
    "admin",
    __name__
)

# ==========================================
# ADMIN DASHBOARD
# ==========================================

@admin.route("/admin-dashboard")
@login_required
def admin_dashboard():

    # ======================================
    # ACCESS CONTROL
    # ======================================

    if current_user.role != "super_admin":

        return "Unauthorized Access"

    # ======================================
    # FETCH DATABASE RECORDS
    # ======================================

    resumes = Resume.query.order_by(
        Resume.id.desc()
    ).all()

    users = User.query.order_by(
        User.id.desc()
    ).all()

    companies = Company.query.order_by(
        Company.id.desc()
    ).all()

    # ======================================
    # ANALYTICS
    # ======================================

    analytics = generate_analytics(
        resumes,
        companies
    )

    # ======================================
    # EXTRA DASHBOARD STATS
    # ======================================

    total_resumes = len(resumes)

    total_users = len(users)

    total_companies = len(companies)

    shortlisted_candidates = len([
        r for r in resumes
        if r.ai_score and r.ai_score >= 70
    ])

    pending_count = len([
        c for c in companies
        if c.status == "pending_request"
    ])

    # ======================================
    # RENDER ADMIN DASHBOARD
    # ======================================

    return render_template(

        "admin/dashboard.html",

        resumes=resumes,

        users=users,

        companies=companies,

        analytics=analytics,

        total_resumes=total_resumes,

        total_users=total_users,

        total_companies=total_companies,

        shortlisted_candidates=shortlisted_candidates,

        pending_count=pending_count
    )