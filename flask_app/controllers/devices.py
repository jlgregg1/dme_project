from flask import Flask, flash, session, render_template, redirect, request, url_for
from flask_app import app
from flask_app.models import user, device, message
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app.config['UPLOAD_FOLDER'] = "static/files"

class UploadFileForm(FlaskForm):
    file = FileField("File", validators = [InputRequired()])
    submit = SubmitField("Upload File")

#visible routes
@app.route("/learn")
def learn():
    if "user_id" not in session: 
        return redirect ("/")
    return render_template("learn.html")

@app.route("/find")
def find():
    if "user_id" not in session: 
        return redirect ("/")
    return render_template("find.html")

@app.route("/post")
def post():
    if "user_id" not in session: 
        return redirect ("/")
    return render_template("post.html")

@app.route("/find_device", methods = ["GET", "POST"])
def find_device():
    if "user_id" not in session: 
        return redirect ("/")
    data = {
        "type" : request.form['type'],
        'zip_code' : request.form['zip_code']
    }
    return render_template("results.html", all_device_results = device.Device.search_results(data))

@app.route("/edit/<int:id>")
def edit(id):
    if "user_id" not in session:
        return redirect ("/")
    data = {
        "device_id" : id #this is the device id, not user id
    }
    return render_template("edit.html", this_device = device.Device.get_device_by_id(data))

#hidden routes

@app.route("/edit_in_db/<int:id>", methods = ['POST'])
def edit_in_db(id):
    if not device.Device.validate_device(request.form):
        return redirect(f'edit_in_db/{id}')
    data = {
        'device_id' : id,
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

@app.route("/add_to_saved_devices/<int:id>", methods = ["POST"]) #need to add a link in the HTML results page
def save_device_in_list(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        'user_id' : session['user_id'],
        'device_id' : id
    }
    device.Device.save_device_in_list(data)
    return redirect("/dashboard")

@app.route("/delete_device/<int:id>")
def delete_from_db(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        "device_id" : id
    }
    device.Device.delete_from_db(data)
    return redirect("/dashboard")

@app.route("/remove/<int:id>")
def remove_from_saved(id):
    if 'user_id' not in session:
        return redirect("/")
    data = {
        "id" : id
    }
    device.Device.remove_from_list(data)
    return redirect("/dashboard")

@app.route('/picture/<int:id>', methods = ["GET", "POST"])
def picture(id):
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(f"/Users/jenniferstewart/Desktop/CodingDojo/projects/dme_project/flask_app/static/files/{secure_filename(file.filename)}")
        photo_url = f"/static/files/{secure_filename(file.filename)}"
        data = {
            "device_id" : id,
            "photo_url" : photo_url
        }
        device.Device.add_photo_url(data)
        return "File has been uploaded"
    return render_template('picture.html', form = form)

