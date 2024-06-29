from . import db

class User(db.Model):
    student_id = db.Column(db.String(20),primary_key=True, nullable =False)
    public_key = db.Column(db.String(255))

class Index_dict(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    keyword = db.Column(db.Text, nullable = False)
    file_id = db.Column(db.Integer, nullable = False)
    owner_student_id = db.Column(db.String(20), nullable = False)

class Delegate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_student_id = db.Column(db.String(20))
    zeta = db.Column(db.String(255))
    secret_password = db.Column(db.String(255))