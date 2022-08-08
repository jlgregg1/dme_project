from flask import Flask, flash, session, render_template, redirect, request
from flask_app import app
from flask_app.models import user, device, message

@app.route("/message/<int:id>")
def display_message_form(id):
    data = {
        "id" : id
    }
    return render_template("message.html", this_device = device.Device.get_device_by_id(data), device_with_owner = device.Device.get_device_owner(data))

@app.route("/add_message_to_db", methods = ["POST"])
def save_message_to_db():
    data = {
        "sender_id" : session['user_id'],
        "device_id" : request.form['device_id'],
        "recipient_id" : request.form['recipient_id'],
        "message" : request.form['message']
    }
    message.Message.add_message_to_db(data)
    return redirect("/dashboard")

@app.route("/reply/<int:id>/<int:id2>")
def reply(id, id2):
    data = {
        "id" : id,
        "device_id" : id2
    }
    return render_template("reply.html", message_recipient = user.User.get_user_by_id(data), this_device = device.Device.get_device_by_id(data))

@app.route("/add_reply_to_db", methods = ["POST"])
def add_reply_to_db():
    data = {
        "sender_id" : session['user_id'],
        "recipient_id" : request.form['recipient_id'],
        "message" :request.form['message'],
        "device_id" : request.form['device_id']
    }
    message.Message.add_message_to_db(data)
    return redirect("/dashboard")
