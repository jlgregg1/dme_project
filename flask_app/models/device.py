from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app # Might need to import the app in certain cases
from flask import flash
import re #import regex module
from flask_app.controllers import devices, users
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Device:
    db = "users_devices"

    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.zip_code = data['zip_code']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @staticmethod
    def validate_device(form_data):
        is_valid = True
        if len(form_data['comments']) < 10: 
            flash("Comments must be 10 or more characters")
            is_valid = False
        if len(form_data['zip_code']) != 5:
            flash("Must enter a 5-digit zip-code")
        return is_valid

    @classmethod
    def add_to_db(cls, data):
        query = "INSERT INTO devices (type, zip_code, comments, user_id) VALUES (%(type)s, %(zip_code)s, %(comments)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def view_users_posted_devices(cls, data):
        query = "SELECT * FROM devices WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return []
        else:
            device_list = []
            for this_device_dictionary in results:
                this_device_object = cls(this_device_dictionary)
                device_list.append(this_device_object)
            return device_list

    @classmethod
    def view_users_saved_devices(cls, data):
        query = "SELECT * FROM devices LEFT JOIN saved_devices ON devices.id = saved_devices.device_id WHERE saved_devices.user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return []
        else:
            device_list = []
            for this_device_dictionary in results:
                this_device_object = cls(this_device_dictionary)
                device_list.append(this_device_object)
            return device_list
    
    @classmethod
    def save_device_in_list(cls, data):
        query = "INSERT INTO saved_devices (device_id, user_id) VALUES(%(device_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def search_results(cls, data):
        query = "SELECT * FROM devices WHERE type = %(type)s AND zip_code = %(zip_code)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return []
        else:
            device_list = []
            for this_device_dictionary in results:
                this_device_object = cls(this_device_dictionary)
                device_list.append(this_device_object)
            return device_list

    @classmethod
    def get_device_by_id(cls, data):
        query = "SELECT * FROM devices WHERE id = %(device_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            this_device_dictionary = results[0]
            this_device_object = cls(this_device_dictionary)
        return this_device_object
    
    @classmethod
    def get_device_owner(cls, data):
        query = "SELECT * FROM devices LEFT JOIN users ON users.id = devices.user_id WHERE devices.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            this_device_dictionary = results[0]
            this_device_object = cls(this_device_dictionary)
            this_user_dictionary = {
                "id" : results[0]['users.id'],
                "first_name" : results[0]['first_name'],
                "last_name" : results[0]['last_name'],
                "email" : results[0]['email'],
                "password" : results[0]['password'],
                "created_at" : results[0]['users.created_at'],
                "updated_at" : results[0]['users.updated_at']
            }
            this_user_object = user.User(this_user_dictionary)
            this_device_object.user = this_user_object
            return this_device_object
    
    @classmethod
    def edit_in_db(cls, data):
        query = "UPDATE devices SET type = %(type)s, zip_code = %(zip_code)s, comments = %(comments)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_from_db(cls, data):
        query = "DELETE FROM devices WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def remove_from_list(cls, data):
        query = "DELETE FROM saved_devices WHERE device_id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)














