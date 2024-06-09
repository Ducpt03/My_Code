from flask import Blueprint, url_for, render_template, request, session, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth",__name__)

# @auth.route('/', methods =["POST","GET"])
# def login():
#     if request.method == 'POST':
#         if 'login' in request.form:
#             email = request.form['email']
#             password = request.form['password']

#         elif 'register' in request.form:
#             username = request.form['new-username']
#             email = request.form['new-email']
#             password = request.form['new-password']

#     return render_template('index.html')

@auth.route("/")
@auth.route("/login", methods = ["POST", "GET"])
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email = email).first()
    if user:
      if check_password_hash(user.password, password):
        session.permanent = True
        login_user(user, remember=True)
        flash("Logged in success!", category="success")
        return redirect(url_for("views.home"))
      else:
        flash("Wrong password! Please check again!", category="error")
    else:
      flash("User doesn't exist!", category="error")
  return render_template("login.html", user = current_user)


@auth.route("/sign-up", methods = ["POST", "GET"])
def sign_up():
  if request.method == "POST":
    user_name = request.form.get("user_name")
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email = email).first()
    if user:
      flash("User existed!", category="error")
    elif len(email) < 4:
      flash("Email must be greater than 3 characters", category="error")
    elif len(password) < 7:
      flash("Password must be greater than 7 characters", category="error")
    else:
      password = generate_password_hash(password,method= "scrypt")
      new_user = User(user_name,email,password)
      try:
        db.session.add(new_user)
        db.session.commit()
        flash("user created!", category="success")
        login_user(user,remember=True)
        return redirect(url_for("views.home"))
      except:
        "error"
  return render_template("sign_up.html", user = current_user)
