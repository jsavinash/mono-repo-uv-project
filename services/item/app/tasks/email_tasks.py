"""
Email Tasks
"""

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from item.app.core.config.settings import settings
from item.app.tasks.celery_app import celery_app

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


@celery_app.task
def send_email_task(email: str, subject: str, body: str):
    """Send email asynchronously"""
    message = MessageSchema(
        subject=subject, recipients=[email], body=body, subtype="html"
    )

    fm = FastMail(conf)
    fm.send_message(message)
    return f"Email sent to {email}"
