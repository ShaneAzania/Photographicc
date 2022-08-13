from flask import flash
from photographicc_app.assets.regex import EMAIL_REGEX
from photographicc_app.config.mysqlconnection import connectToMySQL
from photographicc_app.models import image

class Album:
    db = 'photographicc'
    db_table = 'albums'
    db_table_sub_1 = 'album_with_images'
    db_table_sub_2 = 'images'
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.user = None
        self.images = []
    # **********************************************************************************************************************************
    # create*****************************************************************
    @classmethod
    def create( cls , data ):
        query = "INSERT INTO " + cls.db_table + " ( name, user_id ) VALUES ( %(name)s, %(user_id)s );"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #retreive*****************************************************************
    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM " + cls.db_table + " WHERE user_id = %(user_id)s  ORDER BY name ASC;"
        result =  connectToMySQL(cls.db).query_db(query, data)
        albums =[]
        for x in result:
            albums.append(cls(x))
        return albums
    @classmethod
    def get_one_with_images(cls, data):
        query = "SELECT * FROM " + cls.db_table + " LEFT JOIN " + cls.db_table_sub_1 + " ON albums.id = album_with_images.album_id LEFT JOIN " + cls.db_table_sub_2 + " ON images.id = album_with_images.image_id WHERE " + cls.db_table + ".id = %(id)s;"
        result =  connectToMySQL(cls.db).query_db(query,data)
        album = cls(result[0])
        for img in result:
            img_data = {
                "id": img['images.id'],
                "filename" : img['filename'],
                "keywords" : img['keywords'],
                "created_at" : img['images.created_at'],
                "updated_at" : img['images.updated_at'],
                "user_id" : img['user_id']
            }
            album.images.append(image.Image(img_data))
        return album
    #**********************************************************************************************************************************
    #update*****************************************************************
    # first_name last_name email password age dojo_id
    @classmethod
    def update(cls,data):
        query = "UPDATE "+ cls.db_table +" SET name = %(name)s, updated_at = now() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #delete*****************************************************************
    @classmethod
    def delete (cls, data):
        # delete all the albums_with_images pairs associated with this album
        query = "DELETE FROM " + cls.db_table_sub_1 + " WHERE album_id = %(id)s;"
        connectToMySQL(cls.db).query_db( query, data)
        # delete this album
        query = "DELETE FROM " + cls.db_table + " WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)

    #**********************************************************************************************************************************
    # validate *****************************************************************
    def validateForm(data):
        valid = True
        if len(data['name']) < 3:
            flash('Album name must be longer than 3 characters long.')
            valid = False
        return valid