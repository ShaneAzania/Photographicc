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
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif', 'tiff', 'tif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# END uploading images ***********************************************
# ****************************************************************