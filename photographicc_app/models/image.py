from flask import flash
from photographicc_app.assets.regex import EMAIL_REGEX
from photographicc_app.config.mysqlconnection import connectToMySQL
from photographicc_app.models import album

class Image:
    db = 'photographicc'
    db_table = 'images'
    db_table_sub_1 = 'album_with_images'
    db_table_sub_2 = 'albums'
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.filename = db_data['filename']
        self.keywords = db_data['keywords']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator_user_name = None
        # change file location directory to fit each project
        if db_data['filename']:
            self.location = 'img/image_uploads/' + db_data['filename']
        self.albums = []
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
        query = "SELECT * FROM " + cls.db_table + "  ORDER BY created_at DESC;"
        result =  connectToMySQL(cls.db).query_db(query)
        images =[]
        for x in result:
            images.append(cls(x))
        return images
    @classmethod
    def get_all_by_user(cls, data):
        query = "SELECT * FROM " + cls.db_table + " WHERE user_id = %(id)s  ORDER BY created_at DESC;"
        result =  connectToMySQL(cls.db).query_db(query,data)
        images =[]
        for x in result:
            images.append(cls(x))
        return images
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM " + cls.db_table + " LEFT JOIN " + cls.db_table_sub_1 + " ON images.id = album_with_images.image_id LEFT JOIN " + cls.db_table_sub_2 + " ON albums.id = album_with_images.album_id WHERE " + cls.db_table + ".id = %(id)s;"
        result =  connectToMySQL(cls.db).query_db(query,data)
        # create object of the image
        image = cls(result[0])
        # add each album from the query to the albums array
        # print('IMAGE ALBUMS:')
        for row in result:
            row_data = {
                "id": row['albums.id'],
                "name" : row['name'],
                "created_at" : row['albums.created_at'],
                "updated_at" : row['albums.updated_at'],
                "user_id" : row['user_id']
            }
            image.albums.append(album.Album(row_data))
            # print()
            # print(row_data)
            # print()
        return image
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


    # ALBUMS_WITH_IMAGES
    #**********************************************************************************************************************************
    # add to album *****************************************************************
    @classmethod
    def add_to_album (cls, data):
        # check if the album_with_images pair exist before creating the pair
        query = "SELECT * FROM " + cls.db_table_sub_1 + " WHERE image_id = %(image_id)s AND album_id = %(album_id)s;"
        if not connectToMySQL(cls.db).query_db(query, data):
            # create album_with_images pair
            query = "INSERT INTO " + cls.db_table_sub_1 + " ( image_id, album_id ) VALUES ( %(image_id)s, %(album_id)s );"
            return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    # delete from album *****************************************************************
    @classmethod
    def delete_from_album (cls, data):
        # check if the album_with_images pair exist before creating the pair
        query = "SELECT * FROM " + cls.db_table_sub_1 + " WHERE image_id = %(image_id)s AND album_id = %(album_id)s;"
        if connectToMySQL(cls.db).query_db(query, data):
            # delete album_with_images pair
            query = "DELETE FROM " + cls.db_table_sub_1 + " WHERE image_id = %(image_id)s AND album_id = %(album_id)s;"
            return connectToMySQL(cls.db).query_db( query, data)
    #**********************************************************************************************************************************
    # search for user images by keyword *****************************************************************
    @classmethod
    def search_for_users_images(cls, data):
        # split search string by spaces and put into an search_terms[]
        search_terms = data['search_string'].split(' ')
        # cycle through each word in search_terms[] and check if ALL the search terms are present in an images keywords variables
        imgs = cls.get_all_by_user({'id':data['id']})
        images_that_pass = []
        for img in imgs:
            every_search_word_in_keywords = True
            for word in search_terms:
                if word.lower() not in img.keywords.lower():
                    every_search_word_in_keywords = False
            if every_search_word_in_keywords:
                images_that_pass.append(img)
        return images_that_pass
    #**********************************************************************************************************************************
    # search for images by keyword *****************************************************************
    @classmethod
    def search_for_all_images(cls, data):
        # split search string by spaces and put into an search_terms[]
        search_terms = data['search_string'].split(' ')
        terms_confirmed_in_keywords = []
        for x in search_terms:
            terms_confirmed_in_keywords.append(True)
        # cycle through each word in search_terms[] and check if ALL the search terms are present in an images keywords variables
        imgs = cls.get_all()
        images_that_pass = []
        for img in imgs:
            every_search_word_in_keywords = True
            for word in search_terms:
                if word.lower() not in img.keywords.lower():
                    every_search_word_in_keywords = False
            if every_search_word_in_keywords:
                images_that_pass.append(img)
        return images_that_pass
