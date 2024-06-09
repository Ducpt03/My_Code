from project import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    workID = db.Column(db.String(15), unique = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(300), nullable = False)
    role = db.Column(db.String(20), nullable = False)

    def __init__(self,id,workID,username,email,password,role):
        self.id = id
        self.workID = workID
        self.username = username
        self.email = email
        self.password = password
        self.role = role

# class Document(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     country = db.Column(db.String(100))
#     age = db.Column(db.Integer())
#     index = db.Column(db.String())
#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))




