from app.database import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String, nullable=False)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String, nullable=False)

class HiredEmployee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=True)