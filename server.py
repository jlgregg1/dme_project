#server file runs the app itself
from flask_app import app
from flask_app.controllers import users

if __name__ == "__main__":
    app.run(debug = True)