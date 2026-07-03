from flask import Flask, redirect
import os

from dotenv import load_dotenv

from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from database.db import db
from models.user_model import User
from models.resume_model import Resume
from models.company_model import Company, Invite

from services.email_service import mail

# =====================================
# ENV
# =====================================

load_dotenv()

# =====================================
# APP INIT
# =====================================

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


db_path = os.path.join(BASE_DIR, 'database', 'hr_system.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# =====================================
# MAIL CONFIG
# =====================================
# If MAIL_USERNAME is left unset (no .env values), email_service.py
# automatically falls back to printing emails to the console instead
# of sending them — handy for local development.

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get(
    'MAIL_DEFAULT_SENDER',
    'noreply@talenteon.ai'
)

mail.init_app(app)

# =====================================
# LOGIN MANAGER
# =====================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

# =====================================
# BLUEPRINTS
# =====================================

from routes.auth_routes import auth
from routes.resume_routes import resume
from routes.admin_routes import admin
from routes.compare_routes import compare_bp
from routes.onboarding_routes import onboarding

app.register_blueprint(compare_bp)

app.register_blueprint(auth)
app.register_blueprint(resume)
app.register_blueprint(admin)
app.register_blueprint(onboarding)

# =====================================
# SUPER ADMIN CREATION
# =====================================

def create_super_admin():

    with app.app_context():

        admin = User.query.filter_by(
            role="super_admin"
        ).first()

        if not admin:

            new_admin = User(
                username="admin",
                email="admin@talenteon.ai",
                password=generate_password_hash("admin123"),
                role="super_admin"
            )

            db.session.add(new_admin)
            db.session.commit()

            print("SUPER ADMIN CREATED")

# =====================================
# RUN SETUP
# =====================================

with app.app_context():

    db.create_all()

    create_super_admin()

# =====================================
# MAIN RUN
# =====================================

if __name__ == "__main__":

    app.run(debug=True)
