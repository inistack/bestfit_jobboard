from jobboard.celery_app import celery
from flask_mail import Message
from jobboard.extensions import mail, db


@celery.task
def ping():
    return "pong"


@celery.task
def send_comfirmation_email(application_id, candidate_email, job_title):
    from jobboard.models import Application

    application = db.session.query(Application).filter(application_id == Application.id).first()
    if application is None:
        return f"Application with ID {application_id} not found"

    msg = Message(
        subject=f"Application Confirmation for {job_title}",
        recipients=[candidate_email],
        body=f"Thank you for applying for the position of {job_title}. We have received your application and will review it shortly."
    )
    mail.send(msg)

    application.status = 'email_sent'
    db.session.commit()

    return f"Confirmation email sent to {candidate_email} for job {job_title}"
