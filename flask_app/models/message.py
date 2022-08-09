from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app 
from flask_app.controllers import devices, users, messages
from flask_app.models import user, device
from flask import flash

class Message:
    db = "users_devices"

    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = data['sender']
        self.sender_id = data['sender_id']
        self.recipient = data['recipient']
        self.recipient_id = data['recipient_id']
        self.device_id = data['device_id']

    @classmethod
    def add_message_to_db(cls, data):
        query = "INSERT INTO messages (message, sender_id, recipient_id, device_id) VALUES (%(message)s, %(sender_id)s, %(recipient_id)s, %(device_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all_received_messages(cls, data):
        query = "SELECT users.first_name AS sender, users2.first_name as recipient, message, messages.id as id, messages.created_at as created_at, messages.updated_at as updated_at, sender_id, recipient_id, device_id FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.recipient_id WHERE users2.id = %(id)s ORDER BY created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return []
        else:
            message_list = []
            for this_message_dictionary in results:
                this_message_object = cls(this_message_dictionary)
                message_list.append(this_message_object)
            return message_list
            
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(message_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @staticmethod
    def validate_message(form_data):
        is_valid = True
        if len(form_data['message']) < 3: 
            flash("Message must be 3 or more characters")
            is_valid = False
        return is_valid