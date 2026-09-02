from jobboard.extensions import db

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    pdf_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    job = db.relationship('Job', backref='applications')
    candidate = db.relationship('User', backref='applications')

    def __repr__(self):
        return f"<Application job={self.job_id} candidate={self.candidate_id} status={self.status}>"