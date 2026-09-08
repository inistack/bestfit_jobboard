from jobboard.celery_app import celery
from flask_mail import Message
from jobboard.extensions import mail, db
from flask import render_template
from weasyprint import HTML
from jobboard.storage import save_pdf


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


@celery.task
def generate_application_pdf(application_id):
    from jobboard.models import Application

    application = db.session.query(Application).filter_by(id=application_id).first()
    if application is None:
        return f"Application with ID {application_id} not found"
    
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

    application.pdf_url = filepath
    application.status = 'pdf_ready'
    db.session.commit()

    return f"PDF generated for application {application_id}"