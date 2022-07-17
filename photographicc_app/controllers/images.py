from ast import Not, Try
from crypt import methods
from photographicc_app import app
from flask import flash,render_template,redirect,request,session
from photographicc_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

site_title = 'Photographicc'

#image_upload
@app.route('/image_upload')
def image_upload():
    return render_template('image_upload.html', title = site_title)
@app.route('/image_upload_form', methods = ['POST'])
def image_upload_form():

    return redirect('/user_dash')
