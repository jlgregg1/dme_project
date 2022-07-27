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

    @staticmethod
    def validate_device():
        pass

    @classmethod
    def add_to_db():
        pass

