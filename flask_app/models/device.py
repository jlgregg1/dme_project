from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app # Might need to import the app in certain cases
from flask import flash
import re #import regex module
from flask_app.controllers import devices, users
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)