from flask import Flask, flash, session, render_template, redirect, request
from flask_app import app
from flask_app.models import device, user, message
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    if "user_id" not in session: #do not allow access to dashboard page if not logged in (if user ID not in session)
        return redirect ("/")
    data = {
        "id" : session['user_id']
    }
    this_user = user.User.get_user_by_id(data)
    session['first_name'] = this_user.first_name
    return render_template("welcome.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session: #do not allow access to dashboard page if not logged in (if user ID not in session)
        return redirect ("/")
    data = {
        "id" : session['user_id']
    }
    this_user = user.User.get_user_by_id(data)
    return render_template("dashboard.html", this_user = this_user, all_devices = device.Device.view_users_posted_devices(data), all_saved_devices = device.Device.view_users_saved_devices(data), all_messages = message.Message.get_all_received_messages(data))

#hidden
@app.route("/add_user_to_db", methods = ['POST'])
def add_user_to_db():
    if not user.User.validate_user(request.form):
        return redirect('/') #redirect to index if invalid and display error messages
    hashed_password = bcrypt.generate_password_hash(request.form['password']) #saves encrypted password in variable
    data = {
        "first_name" : request.form['first_name'],
        "last_name": request.form['last_name'],
        "email" : request.form['email'],
        "password" : hashed_password
        }
    session['user_id'] = user.User.save(data) #save user ID in session to reference later to make sure that user is logged in to access certain pages
    return redirect("/welcome")

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] } #create a data dictionary with email from form
    user_in_db = user.User.get_by_email(data) #send data dictionary with email into query to get additional user info
    if not user_in_db: #if the get_by_email returns False, there is no user in db with that email
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): #check to see if hashed passwords match
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id #now have access to all columns in the user table, can be referenced with dot syntax
    return redirect("/welcome") #check to see if /dashboard route works if not logged in (it should not)

@app.route("/logout") #not POST because only clicking a link and not submitting a form
def logout():
    session.clear() #this clears session when user logs out
    return redirect("/")