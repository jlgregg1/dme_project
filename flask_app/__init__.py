from flask import Flask
app = Flask(__name__)
import os

app.secret_key = os.environ.get("FLASK_APP")