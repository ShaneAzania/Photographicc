from ast import Not, Try
from crypt import methods
from fileinput import filename
import mimetypes
from photographicc_app import app
from flask import flash,render_template,redirect,request,session
from werkzeug.utils import secure_filename
from photographicc_app.models.image import Image
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

site_title = 'Photographicc'

#image_upload
@app.route('/image_upload')
def image_upload():
    if 'user_id' in session:
        return render_template('image_upload.html', title = site_title)
    else:
        return redirect('/user_login')
@app.route('/image_upload_form', methods = ['POST'])
def image_upload_form():
    # get image file
    if 'pic_link' in request.form:
        pic_link = request.form['pic_link']
        print()
        print('*******************************************')
        print('*******************************************')
        print('the picture link: ',pic_link)
        print('*******************************************')
        print('*******************************************')
        print()
    else:
        flash('No picture link provided')
        return redirect('/image_upload')
        
    ######################################
    # google drive hosting
    # https://drive.google.com/file/d/<image_id>/view?usp=sharing
    # https://drive.google.com/uc?export=view&id=<image_id>
    # https://drive.google.com/file/d/1_MSAVaOWIfaXSVRtC6dUTdbXr4jD3xKy/view?usp=sharing

    link_strip = pic_link.split('https://drive.google.com/file/d/')
    link_strip = link_strip[1].split('/view?usp=sharing')
    drive_img_id = link_strip[0]
    view_link = f'https://drive.google.com/uc?export=view&id={drive_img_id}'

    data = {
        'link' : view_link,
        'keywords' : request.form['keywords'],
        'user_id': session['user_id']
    }
    Image.create(data)


    return redirect('/user_dash')
# def image_upload_form():  #Failed Image upload to database
#     # get image file
#     if 'pic' in request.files:
#         pic = request.files['pic']
#         print()
#         print('*******************************************')
#         print('*******************************************')
#         print('the picture file: ',pic)
#         print('*******************************************')
#         print('*******************************************')
#         print()
#     else:
#         flash('No picture uploaded')
#         return redirect('/image_upload')
    
#     filename = secure_filename(pic.filename)
#     mimetype = pic.mimetype

#     data = {
#         'filename' : filename,
#         'keywords' : request.form['keywords'],
#         'image_file' : pic.read( ),
#         'mimetype' : mimetype,
#         'user_id': session['user_id']
#     }
#     Image.create(data)


#     return redirect('/user_dash')
