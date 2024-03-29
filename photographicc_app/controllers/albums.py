from crypt import methods
import datetime
from turtle import title
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.album import Album
# from photographicc_app.models import album
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from photographicc_app.assets.repeat_page_elements import nav_render


# Create
@app.route('/album_create')
def album_create():
    if 'user_id' in session:
        return render_template('album_create.html', nav = nav_render())
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
        # Validate
        if Album.validateForm(data):
            album_id = Album.create(data)
            return redirect(f'/album_view/{album_id}')
        else:
            return redirect('/album_create')
    else:
        return redirect('/user_login')
# View
@app.route('/album_view/<int:id>')
def album_view(id):
    album = Album.get_one_with_images({'id': id})
    return render_template('album_view.html', album = album, nav = nav_render())

# Update
@app.route('/album_update_form', methods = ['POST'])
def album_update_form():
    # check if a user is logged in
    if 'user_id' in session:
        data = {
            'id':request.form['id'],
            'name': request.form['name']
        }
        the_album = Album.get_one_with_images(data)
        # check if the logged in user is the owner of this album. If they are, update the album data
        if session['user_id'] == the_album.user_id:
            # Validate
            if Album.validateForm(data):
                Album.update(data)
                return redirect(f'/album_view/{data["id"]}')
            else:
                return redirect(f'/album_view/{data["id"]}')
        else:
            return redirect(f'/album_view/{data["id"]}')
    else:
        return redirect(f'/album_view/{data["id"]}')

# Delete 
@app.route('/album_delete/<int:id>')
def album_delete(id):
    # check if a user is logged in
    if 'user_id' in session:
        the_album = Album.get_one_with_images({'id':id})
        # check if the logged in user is the owner of this album. If they are, update the album data
        if session['user_id'] == the_album.user_id:
            data = {
                'id':id
            }
            Album.delete(data)
            return redirect('/user_dash')
        else:
            return redirect(f'/album_view/{request.form["id"]}')
    else:
        return redirect(f'/album_view/{request.form["id"]}')
