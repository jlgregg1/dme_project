from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app # Might need to import the app in certain cases
from flask import flash
import re #import regex module
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL('user_registration_schema').query_db(query, data)

    @staticmethod
    def validate_user(user_data_from_form):
        is_valid = True
        #check to see if email is already in database to avoid creation of new user with same email
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("user_registration_schema").query_db(query, user_data_from_form)
        if len(results) != 0:
            flash("Email already exists in database", "reg") #second argument is category filter. Make sure it matches the category filter name in the HTML doc's section for "get messages"
            is_valid = False
        if not EMAIL_REGEX.match(user_data_from_form['email']): #check if email meets required format (see regex above)
            flash("Invalid email address!", "reg")
            is_valid = False
        if not PASSWORD_REGEX.match(user_data_from_form['password']): #check to see if password meets required format
            flash("Password must be 8 or more characters and have at least one upper case letter and one number", "reg")
            is_valid = False
        if len(user_data_from_form['first_name']) < 2: #check if first name is >2 letters
            flash("First name must be more than 1 letter", "reg")
            is_valid = False
        if len(user_data_from_form['last_name']) < 2: #check if last name is >2 letters
            flash("Last name must be more than 1 letter", "reg")
            is_valid = False
        if user_data_from_form['password'] != user_data_from_form['confirm_password']: #check if password matches confirm_password field
            is_valid = False
            flash("Passwords must agree", "reg")
        return is_valid #will be a boolean value. This return will be referenced by route functions that ask for validation
    
    @classmethod
    def get_by_email(cls,data): #check to see if email entered is already in db
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('user_registration_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_user_by_id(cls, data): #check to see if id is already in db. Use this function to get additional information if id is known
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('user_registration_schema').query_db(query,data)
        if len(results) == 0:
            return False
        return cls(results[0]) 