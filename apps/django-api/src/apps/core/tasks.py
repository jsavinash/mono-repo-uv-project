from celery import shared_task


@shared_task
def send_email_task(
    subject: str, message: str, recipient_list: list[str]
) -> dict[str, Any]:
    """Send email asynchronously via Celery."""
    from django.core.mail import send_mail

    try:
        send_mail(subject, message, None, recipient_list, fail_silently=False)
        return {"success": True, "recipients": recipient_list}
    except Exception as e:
        return {"success": False, "error": str(e)}
