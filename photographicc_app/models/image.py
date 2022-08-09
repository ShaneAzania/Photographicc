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
        self.filename = db_data['filename']
        self.keywords = db_data['keywords'] #.split(",") #separate by a comma and put into an array
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        # change file location directory to fit each project
        self.location = 'img/image_uploads/' + db_data['filename']
        self.user = None
        self.album = None
    # **********************************************************************************************************************************
    # create*****************************************************************
    @classmethod
    def create( cls , data ):
        query = "INSERT INTO " + cls.db_table + " ( filename, keywords, user_id ) VALUES ( %(filename)s, %(keywords)s, %(user_id)s );"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #retreive*****************************************************************
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM " + cls.db_table + ";"
        result =  connectToMySQL(cls.db).query_db(query)
        images =[]
        for x in result:
            images.append(cls(x))
        return images
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
    # first_name last_name email password age dojo_id
    @classmethod
    def update(cls,data):
        query = "UPDATE "+ cls.db_table +" SET keywords = %(keywords)s, updated_at = now() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    #delete*****************************************************************
    @classmethod
    def delete (cls, data):
        query = "DELETE FROM " + cls.db_table + " WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db( query, data)



