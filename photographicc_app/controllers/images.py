from crypt import methods
import datetime
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.image import Image
# from photographicc_app.models import album
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
site_title = 'Photographicc'

# Upload
@app.route('/image_upload')
def image_upload():
    if 'user_id' in session:
        return render_template('image_upload.html', title = site_title)
    else:
        return redirect('/user_login')
# *****************************************************************************
# uploading images through form ***********************************************
import os
from flask import flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

#This needs to be updated for the host machine/server
UPLOAD_FOLDER = '/Users/shaneazania/Documents/GitHub/Photographicc/photographicc_app/static/img/image_uploads'
#This needs to be updated for the type of file that is expected to be uploaded
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'tif'}
# set the upload folder directory in the app.config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# validate the incoming file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# process the form being received from the client
@app.route('/image_upload_form', methods=['POST'])
def image_upload_form():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/image_upload')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('/image_upload')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) 
            #append dateTime to end of filename before extension
            filename = filename.rsplit('.', 1)[0] + '_' + datetime.datetime.now().strftime("%f") + '.' +filename.rsplit('.', 1)[1].lower()

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data ={
                'filename': filename,
                'keywords' : request.form['keywords'],
                'user_id' : session['user_id']
            }

            # Upload data to database
            Image.create(data)
            # return redirect(url_for('uploaded_file', filename=filename))
            return redirect('/user_dash')
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# END uploading images ***********************************************
# ****************************************************************

# Deleting
@app.route('/image_delete/<int:id>')
def image_delete(id):
    data = {'id' : id}
    img = Image.get_one(data)
    # delet image file from server
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))

    # delete image row from database
    Image.delete(data)

    return redirect('/images_display_all')

# View all images in a pool
@app.route('/images_display_all')
def images_display_all():
    if 'user_id' in session:
        images = Image.get_all()
        return render_template('images_display_all.html', images = images, title = site_title)
    else:
        return redirect('/user_login')
# View one image
@app.route('/image_view/<int:id>')
def image_view(id):
    if 'user_id' in session:
        image = Image.get_one({'id':id})
        return render_template('image_view.html', image = image, title = site_title)
    else:
        return redirect('/user_login')

# Update
@app.route('/image_update_form', methods = ['POST'])
def image_update_form():
    form = request.form
    data = {
        'id':form['id'],
        'keywords': form['keywords']
    }
    Image.update(data)

    return redirect(f'/image_view/{request.form["id"]}')