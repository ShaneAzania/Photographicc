from ast import Not, Try
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

site_title = 'Photographicc'

#Home
@app.route('/')
def index():
    return render_template('index.html', title = site_title)

#Register or Login
@app.route('/login')
def register_login():
    try:
        if int(session['user_id']):
            return redirect('/')
    except:
        return render_template('login.html', title = site_title)
@app.route('/user_register_form', methods = ['POST'])
def user_register_form():
    if User.validate_ninja_form(request.form):
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        user = User.get_one({'id':User.create(data)})
        session.clear()
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
        return redirect('/register_login')
@app.route('/user_login_form', methods = ['POST'])
def user_login_form():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid login')
        return redirect('/register_login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid login')
        return redirect('/register_login')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    session['email'] = user_in_db.email
    return redirect('/sightings_all')
@app.route('/user_logout')
def user_logout():
    session.clear()
    return redirect('/register_login')
