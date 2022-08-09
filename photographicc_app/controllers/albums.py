from crypt import methods
import datetime
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.album import Album
# from photographicc_app.models import album
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
site_title = 'Photographicc'


# Album Create
@app.route('/album_create')
def album_create():
    if 'user_id' in session:
        return render_template('album_create.html', title = site_title)
    else:
        return redirect('/user_login')
# Create Form
@app.route('/album_create_form', methods = ['POST'])
def album_create_form():
    if 'user_id' in session:
        data = {
            'name': request.form['name'],
            'user_id': session['user_id']
        }
        Album.create(data)
        return redirect(f'/user_dash')
    else:
        return redirect('/user_login')
# Update
@app.route('/album_update_form', methods = ['POST'])
def album_update_form():
    form = request.form
    data = {
        'id':form['id'],
        'name': form['name']
    }
    Album.update(data)

    return redirect(f'/image_view/{request.form["id"]}')