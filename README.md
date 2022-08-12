- Using: Python, Javascript, CSS, HTML, Bootstrap (or possibly Skeleton).
- a platform for photographers to upload, organize, share details on, and present their work.
- users can:
	sign-up and edit profile information.
	upload, delete, and add meta data to each post and album.
- git repo link:  https://github.com/ShaneAzania/Photographicc


- The Upload Folder bellow needs to be updated in the 'images.py' controller for the server that this app is hosted on 
- UPLOAD_FOLDER = '/Users/shaneazania/Documents/GitHub/Photographicc/photographicc_app/static/img/image_uploads'
- app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
- Also update " self.location = 'img/image_uploads/' + db_data['filename'] " in the 'image.py' model
