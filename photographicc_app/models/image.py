from sqlite3 import dbapi2
from unittest import result
from flask import flash
from photographicc_app.assets.regex import EMAIL_REGEX
from photographicc_app.config.mysqlconnection import connectToMySQL

class Image:
    db = 'photographicc'
    db_table = 'images'
    db_table_sub_1 = 'users'
    db_table_sub_2 = 'albums'
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.link = db_data['link']
        self.keywords = db_data['keywords']
        self.user_id = db_data['user_id']
        # self.mimetype = db_data['mimetype']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = []
        self.albums = []
        self.album_with_images = []
    # **********************************************************************************************************************************
    # create*****************************************************************
    @classmethod
    def create( cls , data ):
        query = "INSERT INTO " + cls.db_table + " ( link, keywords, user_id ) VALUES ( %(link)s, %(keywords)s, %(user_id)s );"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #retreive*****************************************************************
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM " + cls.db_table + ";"
        result =  connectToMySQL(cls.db).query_db(query)
        users =[]
        for x in result:
            users.append(cls(x))
        return users
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
        query = "UPDATE "+ cls.db_table +" SET keywords = '%(keywords)s', updated_at = now() WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #delete*****************************************************************
    @classmethod
    def delete (cls, data):
        query = "DELETE FROM " + cls.db_table + " WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)