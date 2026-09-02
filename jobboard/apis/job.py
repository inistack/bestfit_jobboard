from flask.views import MethodView
from flask_smorest import Blueprint, abort
from jobboard.schemas.job import JobSchema
from jobboard.models import Job
from jobboard.extensions import db

job_bp = Blueprint('jobs', __name__, description='Job management endpoints')

@job_bp.route('/jobs')
class JobList(MethodView):
    @job_bp.response(200, JobSchema(many=True))
    def get(self):
        """Get a list of all jobs."""
        jobs = db.session.query(Job).all()
        return jobs

    @job_bp.arguments(JobSchema)
    @job_bp.response(201, JobSchema)
    def post(self, new_job_data):
        """Create a new job."""
        new_job = Job(**new_job_data, employer_id=1)
        db.session.add(new_job)
        db.session.commit()
        return new_job
    

@job_bp.route('/jobs/<int:job_id>')
class JobDetail(MethodView):
    @job_bp.response(200, JobSchema)
    def get(self, job_id):
        """Get details of a specific job."""
        job = db.session.query(Job).filter_by(id=job_id).first()
        if job is None:
            abort(404, message=f"Job with ID {job_id} not found")
        return job
    
    @job_bp.arguments(JobSchema(partial=True))
    @job_bp.response(200, JobSchema)
    def put(self, updated_job_data, job_id):
        """Update a specific Job via its ID."""
        job = db.session.query(Job).filter_by(id=job_id).first()
        if job is None:
            abort(404, message=f"Job with ID {job_id} not found")

        for key, value in updated_job_data.items():
            setattr(job, key, value)

        db.session.commit()
        return job
    
    @job_bp.response(204)
    def delete(self, job_id):
        """Delete a specific Job via its ID"""
        job = db.session.query(Job).filter_by(id=job_id).first()
        if job is None:
            abort(404, message=f"Job with ID {job_id} not found")
        
        db.session.delete(job)
        db.session.commit()