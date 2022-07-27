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
    if "user_id" not in session: #do not allow access to create page if not logged in (if user ID not in session)
        return redirect ("/")
    return render_template("post.html")

@app.route("/find_device", methods = ["GET", "POST"])
def find_device():
    if "user_id" not in session: #do not allow access to create page if not logged in (if user ID not in session)
        return redirect ("/")
    data = {
        "type" : request.form['type'],
        'zip_code' : request.form['zip_code']
    }
    return render_template("results.html", all_device_results = device.Device.search_results(data))

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" not in session: #do not allow access to create page if not logged in (if user ID not in session)
        return redirect ("/")
    data = {
        "id" : id
    }
    return render_template("edit.html") #will need to pass in correct device info

#hidden

@app.route("/edit_in_db/<int:id>", methods = ['POST'])
def edit_in_db(id):
    if not device.Device.validate_device(request.form):
        return redirect(f'edit_in_db/{id}')
    data = {
        'id' : id,
        'type' : request.form['type'],
        'zip_code' : request.form['zip_code'],
        'comments' : request.form['comments']
    }
    device.Device.edit_in_db(data)
    return redirect('/dashboard')

@app.route("/add_to_db", methods = ["POST"])
def add_to_db():
    if not device.Device.validate_device(request.form):
        return redirect('/post')
    data = {
        'type' : request.form['type'],
        'zip_code' : request.form['zip_code'],
        'comments' : request.form['comments'],
        'user_id' : session['user_id'] #track who posted it
    }
    device.Device.add_to_db(data)
    return redirect('/dashboard')

@app.route("/add_to_saved_devices/<int:id>") #need to add a link in the HTML results page
def save_device_in_list(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        'user_id' : session['user_id'],
        'device_id' : id
    }
    device.Device.save_device_in_list(data)
    return redirect("/dashboard")

@app.route("/delete_from_db")
def delete_from_db():
    pass
    # return redirect("/dashboard")

@app.route("/remove_from_saved")
def remove_from_saved():
    pass
    # return redirect("/dashboard")