from flask import Flask, request, render_template, redirect, url_for, Blueprint
import os
from flask_sqlalchemy import SQLAlchemy

SECRET_KEY = os.environ.get("KEY")
DB_NAME = os.environ.get("DB_NAME")
DB_PSW = os.environ.get("DB_PSW")

db = SQLAlchemy()

def create_database(app):
    # if not os.path.exists("./projects/project.db"):
    with app.app_context():
        db.create_all() 
        print("Created DB!")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcde123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:abcde123@localhost/project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .models import User
    # app.app_context().push()
    # app.app_context()
    create_database(app)
    from project.auth import auth
    from project.view import view

    app.register_blueprint(auth)
    app.register_blueprint(view)

    return app