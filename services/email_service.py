from flask import current_app, url_for
from flask_mail import Mail, Message

# ==========================================
# MAIL EXTENSION
# ==========================================
# Initialized against the app in app.py via mail.init_app(app)

mail = Mail()


def _dev_mode_enabled():
    """
    If no MAIL_USERNAME is configured (e.g. local development with no
    .env file), we skip real SMTP and print the email to the console
    instead. This lets you build and test the whole onboarding flow
    before wiring up real email credentials.
    """
    return not current_app.config.get("MAIL_USERNAME")


def _print_dev_email(to, subject, body):
    print("=" * 60)
    print("[DEV MODE] No SMTP configured — printing email instead of sending.")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print("-" * 60)
    print(body)
    print("=" * 60)


# ==========================================
# INVITE EMAIL
# ==========================================

def send_invite_email(invite):

    setup_link = url_for(
        "onboarding.onboard_setup",
        token=invite.token,
        _external=True
    )

    subject = "You're invited to set up your TalentEon AI account"

    body = (
        f"Hi {invite.full_name or ''},\n\n"
        f"Your company \"{invite.company.name}\" has been approved on TalentEon AI.\n\n"
        f"Complete your account setup here (this link expires in 72 hours):\n"
        f"{setup_link}\n\n"
        f"— TalentEon AI"
    )

    if _dev_mode_enabled():
        _print_dev_email(invite.email, subject, body)
        return

    msg = Message(
        subject=subject,
        recipients=[invite.email],
        body=body,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )

    mail.send(msg)


# ==========================================
# REJECTION EMAIL
# ==========================================

def send_rejection_email(company):

    subject = "Update on your TalentEon AI request"

    reason_line = (
        f":\n\n{company.rejection_reason}\n\n"
        if company.rejection_reason
        else ".\n\n"
    )

    body = (
        f"Hi {company.contact_name or ''},\n\n"
        f"Thanks for your interest in TalentEon AI. After review, we're unable to "
        f"approve access for \"{company.name}\" at this time" + reason_line +
        "— TalentEon AI"
    )

    if _dev_mode_enabled():
        _print_dev_email(company.contact_email, subject, body)
        return

    msg = Message(
        subject=subject,
        recipients=[company.contact_email],
        body=body,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER")
    )

    mail.send(msg)
