from crypt import methods
import datetime
from turtle import title
from photographicc_app import app
from flask import flash, render_template,redirect,request,session
from photographicc_app.models.image import Image
from photographicc_app.models import album
from photographicc_app.models import user
# from photographicc_app.models import album
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from photographicc_app.assets.repeat_page_elements import nav_render

# Upload
@app.route('/image_upload')
def image_upload():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        return render_template('image_upload.html', albums = album.Album.get_all(data), nav = nav_render())
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
    if 'user_id' in session:
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
                # Upload Image data to database
                image_id = Image.create(data)
                # Creat albums_with_images pair in database
                # get albums from form
                album_ids_from_form = request.form.getlist('albums[]') #array of albums from the form
                # cycle through the albums_from_form and create an albums_with_images pair for each
                for a_id in album_ids_from_form:
                    data = {
                        'image_id': image_id,
                        'album_id' : a_id
                    }
                    Image.add_to_album(data)
                # return redirect(url_for('uploaded_file', filename=filename))
                return redirect(f'/image_view/{image_id}')
# END uploading images ***********************************************
# ****************************************************************

# Deleting
@app.route('/image_delete/<int:id>')
def image_delete(id):
    data = {
        'id' : id,
    }
    img = Image.get_one(data)
    if 'user_id' in session:
        # if user is the owner of this image, allow delete
        if session['user_id'] == img.user_id:
            # delete all rows from albums_with_images with current image
            for a in img.albums:
                Image.delete_from_album({
                    'album_id': a.id,
                    'image_id' : id
                })
            # delete image row from database
            Image.delete(data)
            # delete image file from server
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
            return redirect('/images_display_all')
        else:
            return redirect(f'/image_view/{img.id}')
    else:
        return redirect(f'/image_view/{img.id}')
    

# View all user images in a pool
@app.route('/images_display_all')
def images_display_all():
    if 'user_id' in session:
        images = Image.get_all_by_user({'id':session['user_id']})
        return render_template('images_display_all.html', images = images, nav = nav_render())
    else:
        return redirect('/user_login')
# View all community images in a pool
@app.route('/images_display_all_community')
def images_display_all_community():
        images = Image.get_all()
        # cycle through images and attatch user names
        for img in images:
            this_user = user.User.get_one({'id':img.user_id})
            img.creator_user_name = this_user.user_name
        return render_template('images_display_all_community.html', images = images, nav = nav_render())
# View one image
@app.route('/image_view/<int:id>')
def image_view(id):
    # if logged in user matches image owner user_id, then allow image details to be edited. else, don't all edit 
    image = Image.get_one({'id':id})
    creator = user.User.get_one({'id':image.user_id})
    if 'user_id' in session:
        if session['user_id'] == image.user_id:
            # show all albums created by user
            albums = album.Album.get_all({'user_id':session['user_id']})
            return render_template('image_view.html', image = image, albums = albums, creator = creator, nav = nav_render())
        else:
            # only show albums associated with this image
            albums = image.albums
            return render_template('image_view.html', image = image, albums = albums, creator = creator, nav = nav_render())
    else:
        # only show albums associated with this image
        albums = image.albums
        return render_template('image_view.html', image = image, albums = albums, creator = creator, nav = nav_render())

# Update Form
@app.route('/image_update_form', methods = ['POST'])
def image_update_form():
    # check if user is logged in
    if 'user_id' in session:
        form = request.form
        the_image = Image.get_one({'id':form['id']})
        # check if the logged in user is the owner of this image. If they are, update the image data
        if session['user_id'] == the_image.user_id:
            form_albums = form.getlist('albums[]') #array of albums from the form
            # update image row in database
            img_data = {
                'id':form['id'],
                'keywords': form['keywords']
            }
            Image.update(img_data)
            # delete: compair what's in the albums_with_images table to what's in the form before deleting from albums_with_images
            current_img_albums = Image.get_one({'id': form['id']}).albums
            print()
            print('CURRENT ALBUMS: ')
            for x in current_img_albums:
                print(x.name)
            print()
            for img_a in current_img_albums:
                if img_a.id not in form_albums:
                    delete_from_album_data = {
                        'image_id':form['id'],
                        'album_id': img_a.id
                    }
                    Image.delete_from_album(delete_from_album_data)
            # add to albums
            for a in form_albums:
                add_to_album_data = {
                    'image_id':form['id'],
                    'album_id': a
                }
                Image.add_to_album(add_to_album_data)

            return redirect(f'/image_view/{request.form["id"]}')
        else:
            return redirect(f'/image_view/{request.form["id"]}')
    else:
        return redirect(f'/image_view/{request.form["id"]}')
            

# images_search form for all images on server
@app.route('/images_search', methods=['POST'])
def images_search():
    data = {
        'search_string':request.form['search'],
    }
    # search results (array of image objects)
    images = Image.search_for_all_images(data)
    # cycle through images and attatch user names
    for img in images:
        this_user = user.User.get_one({'id':img.user_id})
        img.creator_user_name = this_user.user_name
    return render_template('images_search_results.html', search_string = request.form['search'], images = images, nav = nav_render({'search_string':data['search_string']}))
# images_user_search form for users own images
@app.route('/images_user_search', methods=['POST'])
def images_user_search():
    if 'user_id' in session:
        data = {
            'search_string':request.form['search'],
            'id':session['user_id']
        }
        # search results (array of image objects)
        images = Image.search_for_users_images(data)
        return render_template('images_search_user_results.html', search_string = request.form['search'], images = images, nav = nav_render({'search_string':data['search_string']}))        