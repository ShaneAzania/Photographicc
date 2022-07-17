from ast import Not, Try
from crypt import methods
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

site_title = 'Photographicc'

#Home
@app.route('/')
def index():
    # session.clear()
    return render_template('index.html', title = site_title)

#join
@app.route('/user_join')
def login():
    try:
        if int(session['user_id']):
            return redirect('/')
    except:
        return render_template('user_join.html', title = site_title)
@app.route('/user_join_form', methods = ['POST'])
def user_register_form():
    if User.validate_ninja_form(request.form):
        data = {
            'user_name' : request.form['user_name'],
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        #  is email address already registered to existing account
        if User.get_by_email({'email': data['email']}):
            flash('Email alread registered to existing user. Please use another email address.')
            print('======UNSUCCESSFUL DATABASE INSERT')
            session['user_name'] = request.form['user_name']
            session['first_name'] = request.form['first_name']
            session['last_name'] = request.form['last_name']
            session['email'] = request.form['email']
            return redirect('/user_join')


        user = User.get_one({'id':User.create(data)})
        session.clear()
        session['user_name'] = user.user_name
        session['user_id'] = user.id
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['email'] = user.email
        return redirect('/')
    else:
        print('======UNSUCCESSFUL DATABASE INSERT')
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        return redirect('/user_join')
# login
@app.route('/user_login')
def user_login():
    return render_template('user_login.html', title = site_title)
@app.route('/user_login_form', methods = ['POST'])
def user_login_form():
    user = User.get_by_email({'email': request.form['email']})
    print('************************************')
    print('************************************')
    print(user.user_name)
    print('************************************')
    print('************************************')
    if user and bcrypt.check_password_hash(user.password, request.form['password']):
        session.clear()
        session['user_name'] = user.user_name
        session['user_id'] = user.id
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['email'] = user.email
        return redirect('/user_dash')
    else:
        session['user_name'] = request.form['user_name']
        session['password'] = request.form['password']
        return redirect('/user_login')
#log out
@app.route('/user_logout')
def user_logout():
    session.clear()
    return redirect('/user_login')

#dash
@app.route('/user_dash')
def user_dash():
    if 'user_id' in session:
        return render_template('user_dash.html', title = site_title)
    else:
        return redirect('/user_login')