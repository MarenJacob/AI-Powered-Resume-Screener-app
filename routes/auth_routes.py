from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

from werkzeug.security import check_password_hash

from models.user_model import User
from models.resume_model import Resume

from services.analytics_service import generate_analytics

auth = Blueprint('auth', __name__)


# ==========================================
# HOME PAGE
# ==========================================

@auth.route("/")
def home():

    return render_template("index.html")


# ==========================================
# REGISTER
# ==========================================
# Self-serve signup has been retired. Companies now go through
# the "Request Access" flow and are onboarded by a system admin.
# This route is kept so any existing links/templates pointing at
# auth.register don't break.

@auth.route("/register", methods=["GET", "POST"])
def register():

    return redirect(url_for("onboarding.request_access"))


# ==========================================
# LOGIN
# ==========================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            # ------------------------------
            # ROLE-BASED REDIRECT
            # ------------------------------

            if user.role == "super_admin":

                return redirect(
                    url_for('admin.admin_dashboard')
                )

            return redirect(
                url_for('auth.dashboard')
            )

        flash(
            "Invalid email or password.",
            "danger"
        )
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/login.html"
    )


# ==========================================
# USER DASHBOARD
# ==========================================

@auth.route("/dashboard")
@login_required
def dashboard():

    resumes = Resume.query.filter_by(
        company_id=current_user.company_id
    ).all()

    users = User.query.filter_by(
        company_id=current_user.company_id
    ).all()

    analytics = generate_analytics(resumes)

    return render_template(
        "dashboard/dashboard.html",
        resumes=resumes,
        users=users,
        analytics=analytics
    )


# ==========================================
# LOGOUT
# ==========================================

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(
        url_for('auth.login')
    )
