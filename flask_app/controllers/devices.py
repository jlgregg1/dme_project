from flask import Flask, flash, session, render_template, redirect, request
from flask_app import app
from flask_app.models import user, device
from flask_app.controllers import users

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/find")
def find():
    return render_template("find.html")

@app.route("/post")
def post():
    return render_template("post.html")

@app.route("/results")
def results():
    return render_template("results.html")

#hidden
@app.route("/add_to_db")
def add_to_db():
    pass
    # return redirect("/dashboard")

@app.route("/add_to_saved_devices")
def add_to_saved_devices():
    pass
    # return redirect("/dashboard")

@app.route("/delete_from_db")
def delete_from_db():
    pass
    # return redirect("/dashboard")

@app.route("remove_from_saved")
def remove_from_saved():
    pass
    # return redirect("/dashboard")