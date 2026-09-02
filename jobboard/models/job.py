from jobboard.extensions import db

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False, index=True)
    tags = db.Column(db.String(255))
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    employer = db.relationship('User', backref='jobs')

    def __repr__(self):
        return f'<Job {self.title} ({self.location})>'