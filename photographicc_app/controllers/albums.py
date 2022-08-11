from crypt import methods
import datetime
from turtle import title
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.album import Album
# from photographicc_app.models import album
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
site_title = 'Photographicc'


# Create
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
        album_id = Album.create(data)
        return redirect(f'/album_view/{album_id}')
    else:
        return redirect('/user_login')
# View
@app.route('/album_view/<int:id>')
def album_view(id):
    album = Album.get_one_with_images({'id': id})
    return render_template('album_view.html', album = album, title = site_title)

# Update
@app.route('/album_update_form', methods = ['POST'])
def album_update_form():
    form = request.form
    data = {
        'id':form['id'],
        'name': form['name']
    }
    Album.update(data)
    return redirect(f'/album_view/{request.form["id"]}')

# Delete 
@app.route('/album_delete/<int:id>')
def album_delete(id):
    data = {
        'id':id
    }
    Album.delete(data)
    return redirect('/user_dash')
