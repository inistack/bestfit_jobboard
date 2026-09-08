from jobboard.celery_app import celery
from flask_mail import Message
from jobboard.extensions import mail, db
from flask import render_template
from weasyprint import HTML
from jobboard.storage import save_pdf


@celery.task
def ping():
    return "pong"


@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def send_confirmation_email(self, application_id, candidate_email, job_title):
    from jobboard.models import Application

    application = db.session.query(Application).filter(application_id == Application.id).first()
    if application is None:
        return f"Application with ID {application_id} not found"
    
    try:

        msg = Message(
            subject=f"Application Confirmation for {job_title}",
            recipients=[candidate_email],
            body=f"Thank you for applying for the position of {job_title}. We have received your application and will review it shortly."
        )
        mail.send(msg)
    except Exception as e:
        if self.request.retries >= self.max_retries:
            application.status = 'failed'
            db.session.commit()
            return f'Email failed permanently for application {application_id}: {e}'

        countdown = 2 ** self.request.retries
        raise self.retry(exc=e, countdown=countdown)


    application.status = 'email_sent'
    db.session.commit()

    return f"Confirmation email sent to {candidate_email} for job {job_title}"


@celery.task(bind=True, max_retries=3, default_retry_delay=5)
def generate_application_pdf(self, application_id):
    from jobboard.models import Application

    application = db.session.query(Application).filter_by(id=application_id).first()
    if application is None:
        return f"Application with ID {application_id} not found"
    try:
        html_content = render_template(
            'application_pdf.html',
            candidate_name=application.candidate.name,
            candidate_email=application.candidate.email,
            job_title= application.job.title,
            job_location=application.job.location,
            submitted_at=application.created_at.strftime('%Y-%m-%d %H:%M'),
            cover_letter=application.cover_letter
        )

        pdf_bytes = HTML(string=html_content).write_pdf()
        filename = f"application_{application_id}.pdf"
        filepath = save_pdf(filename, pdf_bytes)
    except Exception as e:
        if self.request.retries >= self.max_retries:
            application.status = 'failed'
            db.session.commit()
            return f'PDF generation failed permanently for application {application_id}: {e}'

        countdown = 2 ** self.request.retries
        raise self.retry(exc=e, countdown=countdown)

    application.pdf_url = filepath
    application.status = 'pdf_ready'
    db.session.commit()

    return f"PDF generated for application {application_id}"