from flask import Blueprint, render_template,session,redirect,url_for,request,current_app as app,jsonify, flash
import requests
from .. import db
from ..models import User, manageKey, getFile
from flask_login import login_required
from .service import trapdoor, get_keywords_list
from ..algo import fix_params

user = Blueprint('user', __name__)

param = app.config['PARAM']
g= app.config['G']
params = fix_params(param,g)


@user.route("/user_dashboard/")
@login_required
def user_dashboard():
    role = session.get('role')
    print(role)
    if 'user' in session or role == 'data_user':
        return render_template('data_user/base.html')
    return redirect(url_for('auth.logout'))

@user.route("/user_dashboard/query", methods = ['POST','GET'])
@login_required
def query():
    if request.method == 'POST':
        keyword = str(request.form.get('key_word'))
        owner_student_id = request.form.get('owner_student_id')
        password = request.form.get('secret')
        # keyword = get_keywords_list(keyword_str)
        # print('cl:',keyword)
        Td = trapdoor(params,keyword)
        # print('td:',Td)
        response = requests.post(f"{app.config['PROXY_URL']}/api/query",json={
            'owner_student_id': owner_student_id,
            'password': password,
            'td': str(Td)
        })
        files = []
        if response.status_code == 200:
            data = response.json()
            matches = data
            for match in matches:
                response_query = requests.post(f"{app.config['DATABASE_URL']}/query", json={
                    'match': match
                })
                if response_query.status_code == 200:
                    data = response_query.json()
                    file_title = data['title']
                    file_name = data['file_name']
                    file_content = data['content']
                    owner_name = data['owner_name']
                    file = getFile(match,file_title,file_name,file_content,owner_name)
                    files.append(file)
            return render_template('data_user/search.html',files = files)
    return render_template('data_user/search.html')

@user.route('/user_dashboard/req_key_gen', methods = ['POST','GET'])
@login_required
def pair_key_gen():
    student_id = session.get('student_id')
    user = User.query.filter_by(student_id = student_id).first()
    key = manageKey.query.filter_by(user_id = user.id).first()
    if request.method == 'POST' and not key:
        if not user.is_keygen:
            data = {
                'student_id': student_id
            }
            response = requests.post(f"{app.config['TA_URL']}/ta_dashboard/user_keygen", json = data)
            if response.status_code == 200:
                key = response.json()
                public_key = key['public_key']
                private_key = key['private_key']
                user.is_keygen = True
                session['private_key'] = private_key
                session['public_key'] = public_key  
                newKeyMan = manageKey(user_id = user.id,public_key = public_key,private_key=private_key)
                db.session.add(newKeyMan)
                db.session.commit()
                flash('Key gen successful!','success')
            else:
                return jsonify('Error to generate key'),404
    elif key:
        session['private_key'] = key.private_key
        session['public_key'] = key.public_key  
    return render_template('data_user/keygen.html', user = user,key=key)
