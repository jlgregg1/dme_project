from flask import Flask, flash, request, redirect, render_template
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_APP")
