from flask_login import UserMixin

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.db import db


# ==========================================
# USER MODEL
# ==========================================
# Note: Company now lives in models/company_model.py

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    full_name = db.Column(
        db.String(150),
        nullable=True
    )

    username = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(300),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        default="hr_manager"
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id')
    )

    company = db.relationship(
        'Company',
        backref='users'
    )

    # ======================================
    # PASSWORD HASHING
    # ======================================

    def set_password(self, password):

        self.password = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password,
            password
        )
