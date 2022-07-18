from sqlite3 import dbapi2
from unittest import result
from flask import flash
from photographicc_app.assets.regex import EMAIL_REGEX
from photographicc_app.config.mysqlconnection import connectToMySQL
from photographicc_app.models import album

class Image:
    db = 'photographicc'
    db_table = 'images'
    db_table_sub_1 = 'users'
    db_table_sub_2 = 'albums'
    db_table_mm = 'album_with_images'
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.link = db_data['link']
        self.keywords = db_data['keywords']
        self.user_id = db_data['user_id']
        # self.mimetype = db_data['mimetype']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.albums = []
    # **********************************************************************************************************************************
    # create*****************************************************************
    @classmethod
    def create( cls , data ):
        query = "INSERT INTO " + cls.db_table + " ( link, keywords, user_id ) VALUES ( %(link)s, %(keywords)s, %(user_id)s );"
        image_id = connectToMySQL(cls.db).query_db( query, data)
        album.Album.add_images({"album_id": data['album_id'], "image_id": image_id})
        return image_id
    #**********************************************************************************************************************************
    #retreive*****************************************************************
    @classmethod
    def get_all(cls, data): #{'user_id':user_id}
        query = "SELECT * FROM " + cls.db_table + "WHERE user_id = %(user_id)s;"
        result =  connectToMySQL(cls.db).query_db(query,data)
        return result
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM " + cls.db_table + " WHERE id = %(id)s;"
        result =  connectToMySQL(cls.db).query_db(query,data)
        if result: 
            return cls(result[0])
        else:
            print('Not in database')
            return result
    #**********************************************************************************************************************************
    #update*****************************************************************
    @classmethod
    def update(cls,data):
        query = "UPDATE "+ cls.db_table +" SET keywords = %(keywords)s, updated_at = now() WHERE id = %(id)s;"
        album.Album.change_album(
            {
                "album_id": data['album_id'],
                "image_id": data['id'],
                "current_album_id": data['current_album_id']
            }
        )
        connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #delete*****************************************************************
    @classmethod
    def delete (cls, data):
        # delete current albums_with_images pair for this image
        query = "DELETE FROM " + cls.db_table_mm + " WHERE album_id = %(album_id)s AND image_id = %(image_id)s;"
        connectToMySQL(cls.db).query_db( query, data)

        query = "DELETE FROM " + cls.db_table + " WHERE id = %(image_id)s;"
        return connectToMySQL(cls.db).query_db( query, data)