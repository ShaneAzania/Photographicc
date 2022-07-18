from photographicc_app import app
from flask import flash,render_template,redirect,request,session
from photographicc_app.models.album import Album
site_title = 'Photographicc'

#create album
@app.route('/album_create')
def album_create():
    if 'user_id' in session:
        return render_template('album_create.html', title = site_title)
    else:
        return redirect('/user_login')
@app.route('/album_create_form', methods = ['POST'])
def album_create_form():
    # get image file
    if 'name' not in request.form:
        flash('No album name provided')
        return redirect('/album_create')
    
    data = {
        'name' : request.form['name'],
        'user_id': session['user_id']
    }
    Album.create(data)


    return redirect('/user_dash')

#edit album
@app.route('/album_edit/<int:id>')
def album_edit(id):
    if 'user_id' in session:
        album = Album.get_one_with_images({'id':id, 'user_id' : session['user_id']})
        return render_template('album_edit.html', album = album, title = site_title)
    else:
        return redirect('/user_login')
@app.route('/album_edit_form', methods = ['POST'])
def album_edit_form():
    # get image file
    if 'name' not in request.form:
        flash('No album name provided')
        return redirect('/album_create')
    
    data = {
        'id': request.form['id'],
        'name' : request.form['name'],
        'user_id': session['user_id']
    }
    Album.update(data)


    return redirect('/user_dash')
# delete
@app.route('/album_delete/<int:id>')
def album_delete(id):
    print('ID: ',id)
    data = {
        'id': id,
        'album_id': id,
        'user_id': session['user_id'],
    }
    album = Album.get_one_with_images(data)
    data['images'] = album.images
    Album.delete(data)

    return redirect(f'/user_dash')
    # return redirect('/user_dash')