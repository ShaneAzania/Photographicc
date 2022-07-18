from sqlite3 import dbapi2
from unittest import result
from flask import flash
from photographicc_app.assets.regex import EMAIL_REGEX
from photographicc_app.config.mysqlconnection import connectToMySQL
from photographicc_app.models import image

class Album:
    db = 'photographicc'
    db_table = 'albums'
    db_table_sub = 'images'
    db_table_mm = 'album_with_images'
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
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
    def get_all(cls, data): #{'user_id':user_id}
        query = "SELECT * FROM " + cls.db_table + " WHERE user_id = %(user_id)s;"
        result =  connectToMySQL(cls.db).query_db(query,data)
        return result
    @classmethod
    def get_one_with_images(cls, data):
        #        SELECT * FROM     albums           LEFT JOIN     album_with_images   ON     albums.id           =     album_with_images.album_id   LEFT JOIN     images               ON    images.id              =     album_with_images.image_id   WHERE     albums.user_id           = 6           AND albums.id = 1;;
        query = "SELECT * FROM " + cls.db_table + " LEFT JOIN " + cls.db_table_mm + " ON " + cls.db_table + ".id = " + cls.db_table_mm + ".album_id LEFT JOIN " + cls.db_table_sub + " ON "+ cls.db_table_sub +".id = " + cls.db_table_mm + ".image_id WHERE " + cls.db_table + ".user_id = %(user_id)s AND "+ cls.db_table +".id = %(id)s;"
        results = connectToMySQL(cls.db).query_db( query , data )
        # print(results)
        # results will be a list of topping objects with the burger attached to each row. 
        album = cls( results[0] )
        for row in results:
            # print(row)
            image_data = {
                "id": row["images.id"],
                "link": row["link"],
                "keywords": row["keywords"],
                "user_id" : row["user_id"],
                "created_at" : row['images.created_at'],
                "updated_at" : row['images.updated_at']
            }
            album.images.append( image.Image( image_data ) )
        return album
    #**********************************************************************************************************************************
    #update*****************************************************************
    @classmethod
    def update(cls,data):
        query = "UPDATE "+ cls.db_table +" SET name = '%(name)s', updated_at = now() WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #delete*****************************************************************
    @classmethod
    def delete (cls, data):
        query = "DELETE FROM " + cls.db_table + " WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)

    #**********************************************************************************************************************************
    # add images | album_with_images *****************************************************************
    @classmethod
    def add_images( cls , data ):
        query = "INSERT INTO " + cls.db_table_mm + " ( album_id, image_id ) VALUES ( %(album_id)s, %(image_id)s );"
        return connectToMySQL(cls.db).query_db( query, data)
    # edit change image album | album_with_images *****************************************************************
    @classmethod
    def change_album( cls , data ):
        # Check for current album
        current_album = data['current_album_id'] 
        next_album = data['album_id']

        # delete current albums_with_images pair for this image
        query = "DELETE FROM " + cls.db_table_mm + " WHERE album_id = "+ current_album +" AND image_id = %(image_id)s;"
        connectToMySQL(cls.db).query_db( query, data)
        
        query = "INSERT INTO " + cls.db_table_mm + " ( album_id, image_id ) VALUES ( %(album_id)s, %(image_id)s );"
        connectToMySQL(cls.db).query_db( query, data)
        return None