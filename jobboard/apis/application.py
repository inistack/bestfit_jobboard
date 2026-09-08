from flask.views import MethodView
from flask_smorest import abort, Blueprint
from jobboard.schemas.application import ApplicationSchema, ApplicationStatusSchema
from jobboard.models import Application, Job, User
from jobboard.extensions import db, limiter
from jobboard.utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity
from jobboard.tasks import send_comfirmation_email, generate_application_pdf
from celery import chain

appl_bp = Blueprint('applications', __name__, description='Job application endpoints')

@appl_bp.route('/applications')
class ApplicationList(MethodView):

    @role_required('candidate')
    @appl_bp.response(200, ApplicationSchema(many=True))
    def get(self):
        candidate_id = get_jwt_identity()
        candidate_applications = db.session.query(Application).filter(Application.candidate_id==candidate_id).all()
        return candidate_applications
    
    @limiter.limit("10 per hour")
    @role_required('candidate')
    @appl_bp.arguments(ApplicationSchema)
    @appl_bp.response(201, ApplicationSchema)
    def post(self, application_data):
        job = db.session.query(Job).filter(Job.id==application_data['job_id']).first()
        if job is None:
            abort(404, message='Job not found')
        
        candidate_id = get_jwt_identity()
        application = Application(candidate_id=candidate_id, job_id=application_data['job_id'], cover_letter=application_data['cover_letter'])
        db.session.add(application)
        db.session.commit()
        candidate = db.session.query(User).filter(User.id==candidate_id).first()
        pipeline = chain(
            send_comfirmation_email.s(application.id, candidate.email, job.title),
            generate_application_pdf.si(application.id)
        )
        pipeline.delay()
        return application
        

@appl_bp.route('/applications/<int:application_id>')
class ApplicationDetail(MethodView):

    @role_required('candidate')
    @appl_bp.response(200, ApplicationSchema)
    def get(self, application_id):
        application = db.session.query(Application).filter(Application.id == application_id).first()
        if application is None:
            abort(404, message='Application not found')
        
        candidate_id = get_jwt_identity()
        if application.candidate_id != int(candidate_id):
            abort(403, message='Not your application')
        
        return application


@appl_bp.route('/applications/<int:application_id>/status')
class ApplicationStatus(MethodView):
    @role_required('candidate')
    @appl_bp.response(200, ApplicationStatusSchema)
    def get(self, application_id):
        application = db.session.query(Application).filter_by(id=application_id).first()
        if application is None:
            abort(404, message='Application not found')

        candidate_id = get_jwt_identity()
        if application.candidate_id != int(candidate_id):
            abort(403, message='Not your application')
        
        return application