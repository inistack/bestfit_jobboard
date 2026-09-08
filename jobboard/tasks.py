from jobboard.celery_app import celery
from flask_mail import Message
from jobboard.extensions import mail


@celery.task
def ping():
    return "pong"


@celery.task
def send_comfirmation_email(candidate_email, job_title):
    msg = Message(
        subject=f"Application Confirmation for {job_title}",
        recipients=[candidate_email],
        body=f"Thank you for applying for the position of {job_title}. We have received your application and will review it shortly."
    )
    mail.send(msg)
    return f"Confirmation email sent to {candidate_email} for job {job_title}"
