from datetime import datetime, timedelta
import secrets

from database.db import db


# ==========================================
# COMPANY MODEL
# ==========================================

class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # ======================================
    # ONBOARDING STATUS
    # ======================================
    # pending_request -> submitted, awaiting admin review
    # rejected        -> admin declined the request
    # pending_setup   -> approved, waiting on invited HR admin to set a password
    # active          -> fully onboarded, can log in and use the platform
    # suspended       -> access revoked by admin

    status = db.Column(
        db.String(30),
        default="pending_request",
        nullable=False
    )

    # ======================================
    # REQUEST DETAILS (collected on the public "Request Access" form)
    # ======================================

    contact_name = db.Column(db.String(150))
    contact_email = db.Column(db.String(150))
    company_size = db.Column(db.String(50))
    hiring_needs = db.Column(db.Text)

    # ======================================
    # REVIEW TRAIL
    # ======================================

    reviewed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    reviewed_at = db.Column(db.DateTime)

    rejection_reason = db.Column(db.Text)


# ==========================================
# INVITE MODEL
# ==========================================
# Single-use, time-limited tokens that let an approved company's
# first HR admin (or later teammates) set a password and activate.

class Invite(db.Model):

    __tablename__ = "invites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    token = db.Column(
        db.String(128),
        unique=True,
        nullable=False
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("companies.id"),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    full_name = db.Column(db.String(150))

    role = db.Column(
        db.String(50),
        default="hr_manager"
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False
    )

    used = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    company = db.relationship(
        "Company",
        backref="invites"
    )

    # ======================================
    # HELPERS
    # ======================================

    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    @classmethod
    def create_for_company(cls, company, email, full_name=None, role="hr_manager", hours_valid=72):

        invite = cls(
            token=cls.generate_token(),
            company_id=company.id,
            email=email,
            full_name=full_name,
            role=role,
            expires_at=datetime.utcnow() + timedelta(hours=hours_valid)
        )

        db.session.add(invite)
        db.session.commit()

        return invite
