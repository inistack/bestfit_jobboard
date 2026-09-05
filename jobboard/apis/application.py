from flask.views import MethodView
from flask_smorest import abort, Blueprint
from jobboard.schemas.application import ApplicationSchema
from jobboard.models import Application, Job
from jobboard.extensions import db
from jobboard.utils.decorators import role_required
from flask_jwt_extended import get_jwt_identity

appl_bp = Blueprint('applications', __name__, description='Job application endpoints')

@appl_bp.route('/applications')
class ApplicationList(MethodView):

    @role_required('candidate')
    @appl_bp.response(200, ApplicationSchema(many=True))
    def get(self):
        candidate_id = get_jwt_identity()
        candidate_applications = db.session.query(Application).filter(Application.candidate_id==candidate_id).all()
        return candidate_applications
    
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
        

@appl_bp.route('/applications/<int:application_id>')
class ApplicationDetail(MethodView):

    @role_required('candidate')
    @appl_bp.response(200, ApplicationSchema)
    def get(self, application_id):
        application = db.session.query(Application).filter(Application.id == application_id).first()
        if application is None:
            abort(404, message='Application not found')
        
        candidate_id = get_jwt_identity()
        if application.candidate_id != candidate_id:
            abort(403, message='Not your application')
        
        return application
