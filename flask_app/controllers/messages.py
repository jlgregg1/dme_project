from flask import Flask, flash, session, render_template, redirect, request
from flask_app import app
from flask_app.models import user, device, message

@app.route("/message/<int:id>")
def display_message_form(id):
    if "user_id" not in session: 
        return redirect ("/")
    data = {
        "device_id" : id
    }
    return render_template("message.html", this_device = device.Device.get_device_by_id(data), device_with_owner = device.Device.get_device_owner(data))

@app.route("/reply/<int:id>/<int:id2>")
def reply(id, id2):
    if "user_id" not in session: 
        return redirect ("/")
    data = {
        "id" : id,
        "device_id" : id2
    }
    return render_template("reply.html", message_recipient = user.User.get_user_by_id(data), this_device = device.Device.get_device_by_id(data), all_messages = message.Message.get_all_received_messages(data))

#hidden routes
@app.route("/add_message_to_db/<int:id>", methods = ["POST"])
def save_message_to_db(id):
    if not message.Message.validate_message(request.form):
        return redirect(f'/message/{id}')
    data = {
        "sender_id" : session['user_id'],
        "device_id" : request.form['device_id'],
        "recipient_id" : request.form['recipient_id'],
        "message" : request.form['message']
    }
    message.Message.add_message_to_db(data)
    return redirect("/dashboard")

@app.route("/add_reply_to_db/<int:id>/<int:id2>", methods = ["POST"])
def add_reply_to_db(id, id2):
    if not message.Message.validate_message(request.form):
        return redirect(f'/reply/{id}/{id2}')
    data = {
        "sender_id" : session['user_id'],
        "recipient_id" : request.form['recipient_id'],
        "message" :request.form['message'],
        "device_id" : request.form['device_id']
    }
    message.Message.add_message_to_db(data)
    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):
    data = {
        "message_id" : id
    }
    message.Message.delete(data)
    return redirect("/dashboard")