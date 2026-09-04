from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_smorest.pagination import PaginationParameters
from jobboard.schemas.job import JobSchema, JobQueryArgsSchema, JobUpdateSchema
from jobboard.models import Job
from jobboard.extensions import db
from jobboard.utils.decorators import role_required

job_bp = Blueprint('jobs', __name__, description='Job management endpoints')

@job_bp.route('/jobs')
class JobList(MethodView):
    @job_bp.arguments(JobQueryArgsSchema, location='query')
    @job_bp.response(200, JobSchema(many=True))
    @job_bp.paginate()
    def get(self, query_args, pagination_parameters: PaginationParameters):
        """Get a list of all jobs."""
        query = db.session.query(Job)
        if 'title' in query_args:
            query = query.filter(Job.title.ilike(f"%{query_args['title']}%"))
        if 'location' in query_args:
            query = query.filter(Job.location.ilike(f"%{query_args['location']}%"))
        if 'tags' in query_args:
            query = query.filter(Job.tags.ilike(f"%{query_args['tags']}%"))

        total = query.count()
        pagination_parameters.item_count = total
        query = query.limit(pagination_parameters.page_size).offset(
            (pagination_parameters.page - 1) * pagination_parameters.page_size
        )

        jobs = query.all()
        return jobs

    @role_required('employer')
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

    @role_required('employer')
    @job_bp.arguments(JobUpdateSchema(partial=True))
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
    
    @role_required('employer')
    @job_bp.response(204)
    def delete(self, job_id):
        """Delete a specific Job via its ID"""
        job = db.session.query(Job).filter_by(id=job_id).first()
        if job is None:
            abort(404, message=f"Job with ID {job_id} not found")
        
        db.session.delete(job)
        db.session.commit()