from datetime import datetime

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required
from flask_login import current_user

from database.db import db

from models.company_model import Company
from models.company_model import Invite
from models.user_model import User

from services.email_service import send_invite_email
from services.email_service import send_rejection_email

onboarding = Blueprint("onboarding", __name__)


# ==========================================
# PUBLIC: REQUEST ACCESS
# (replaces open self-serve registration)
# ==========================================

@onboarding.route("/request-access", methods=["GET", "POST"])
def request_access():

    if request.method == "POST":

        company_name = request.form.get("company_name")
        contact_name = request.form.get("contact_name")
        contact_email = request.form.get("contact_email")
        company_size = request.form.get("company_size")
        hiring_needs = request.form.get("hiring_needs")

        existing = Company.query.filter_by(
            name=company_name
        ).first()

        if existing:
            flash("A request for this company already exists.", "danger")
            return redirect(url_for("onboarding.request_access"))

        company = Company(
            name=company_name,
            contact_name=contact_name,
            contact_email=contact_email,
            company_size=company_size,
            hiring_needs=hiring_needs,
            status="pending_request"
        )

        db.session.add(company)
        db.session.commit()

        flash(
            "Thanks! Your request has been submitted. We'll email you once it's reviewed.",
            "success"
        )
        return redirect(url_for("auth.login"))

    return render_template("request_access.html")


# ==========================================
# ADMIN: PENDING COMPANIES QUEUE
# ==========================================

@onboarding.route("/admin/pending-companies")
@login_required
def pending_companies():

    if current_user.role != "super_admin":
        return "Unauthorized Access"

    pending = Company.query.filter_by(
        status="pending_request"
    ).order_by(
        Company.created_at.desc()
    ).all()

    return render_template(
        "admin/pending_companies.html",
        companies=pending
    )


# ==========================================
# ADMIN: APPROVE
# ==========================================

@onboarding.route("/admin/pending-companies/<int:company_id>/approve", methods=["POST"])
@login_required
def approve_company(company_id):

    if current_user.role != "super_admin":
        return "Unauthorized Access"

    company = Company.query.get_or_404(company_id)

    company.status = "pending_setup"
    company.reviewed_by = current_user.id
    company.reviewed_at = datetime.utcnow()

    db.session.commit()

    invite = Invite.create_for_company(
        company=company,
        email=company.contact_email,
        full_name=company.contact_name,
        role="hr_manager"
    )

    send_invite_email(invite)

    flash(
        f"{company.name} approved. Invite sent to {company.contact_email}.",
        "success"
    )
    return redirect(url_for("onboarding.pending_companies"))


# ==========================================
# ADMIN: REJECT
# ==========================================

@onboarding.route("/admin/pending-companies/<int:company_id>/reject", methods=["POST"])
@login_required
def reject_company(company_id):

    if current_user.role != "super_admin":
        return "Unauthorized Access"

    company = Company.query.get_or_404(company_id)

    company.status = "rejected"
    company.reviewed_by = current_user.id
    company.reviewed_at = datetime.utcnow()
    company.rejection_reason = request.form.get("reason")

    db.session.commit()

    send_rejection_email(company)

    flash(f"{company.name} rejected.", "info")
    return redirect(url_for("onboarding.pending_companies"))


# ==========================================
# TOKEN-BASED ACCOUNT SETUP
# (public route, but useless without a valid token)
# ==========================================

@onboarding.route("/onboard/<token>", methods=["GET", "POST"])
def onboard_setup(token):

    invite = Invite.query.filter_by(token=token).first()

    if not invite or invite.used or invite.is_expired:
        flash("This invite link is invalid or has expired.", "danger")
        return redirect(url_for("auth.login"))

    company = invite.company

    if request.method == "POST":

        full_name = request.form.get("full_name") or invite.full_name
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not password or password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("onboarding.onboard_setup", token=token))

        existing_user = User.query.filter_by(email=invite.email).first()

        if existing_user:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("auth.login"))

        username = invite.email.split("@")[0]

        new_user = User(
            full_name=full_name,
            username=username,
            email=invite.email,
            role=invite.role,
            company_id=company.id
        )

        new_user.set_password(password)

        invite.used = True
        company.status = "active"

        db.session.add(new_user)
        db.session.commit()

        flash("Account created! You can now log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template(
        "onboard_setup.html",
        invite=invite,
        company=company
    )
