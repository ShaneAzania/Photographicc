from ast import Not, Try
from crypt import methods
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.user import User
from photographicc_app.models import album
from photographicc_app.models import image
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from photographicc_app.assets.repeat_page_elements import nav_render


# # nav data
# nav_data = {}
# if 'user_id' in session:
#     nav_data = {
#         'search_string': '',
#         'user_id': session["user_id"],
#         'user_name': session["user_name"]
#     }
# else:
#     nav_data = {
#         'search_string': '',
#     }

#Home
@app.route('/')
def index():
    data = {
        'lower': 0,
        'upper': 24
    }
    # images  = image.Image.get_all()
    images  = image.Image.get_all_in_range(data)
    return render_template('index.html', nav = nav_render(), images = images)

#join
@app.route('/user_join')
def join():
    try:
        if int(session['user_id']):
            return redirect('/')
    except:
        return render_template('user_join.html', nav = nav_render())
@app.route('/user_join_form', methods = ['POST'])
def user_register_form():
    if User.validate_form(request.form):
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

        #create user and set current user in session
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
    if 'user_id' in session:
        return redirect('/user_dash')
    return render_template('user_login.html', nav = nav_render())
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

#dash / MyAlbums
@app.route('/user_dash')
def user_dash():
    if 'user_id' in session:
        # get albums
        albums = album.Album.get_all({'user_id': session['user_id']})
        # get images for albums
        albums_with_images = []
        for a in albums:
            albums_with_images.append(album.Album.get_one_with_images({ 'id': a.id}))
        
        return render_template('user_dash.html', albums = albums_with_images, nav = nav_render())
    else:
        return redirect('/user_login')