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

#get album with images