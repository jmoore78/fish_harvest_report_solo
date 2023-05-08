from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.report import Report
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#----render form route
@app.route('/')
def home_page():
    return render_template("index.html")

#----post route "get form info and do something with it" 
@app.route('/register', methods=['POST']) # registration validation
def register():
    if not User.validate_registration(request.form): #redirects to the registration page if the provided info is not valid
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # hash the password before storing it in the database
    print(pw_hash) # for dev-visual security verification test
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save(data) # Call the save User @classmethod on the object to create. data will be the object and the info is taken from the form.
    session['user_id'] = user_id # store user id into session. id comes from pymysql which will return the id of the newly created row (save method from user.py)
    return redirect('/dashboard')

#----authentication
@app.route('/login', methods=['POST']) # login validation
def login():
    data = { "email" : request.form['email'] } # see if the email provided as a username exists in the database
    user_in_db = User.get_by_email(data) # class method from user to validate the email is already registered and in the databse from the registration step
    if not user_in_db: # if user is not registered in the db
        flash("Invalid Email/Password","login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): # if we get False after checking the password, flash shows error message
        flash("Invalid Email/Password","login")
        return redirect('/')
    session['user_id'] = user_in_db.id # if the passwords matched, we set the user_id into session
    print(session['user_id'])
    return redirect('/dashboard')

@app.route('/logout')# logs user out and clears the session id so the user cannot get back in without logging in again
def logout():
    session.pop('user_id', None) # Session class is a wrapper around a python Dict. used default None to prevent a KeyError exception
    flash("Logout Successful", "logout")
    return redirect('/') # redirected to the log in page

#----renders something to the user 
@app.route('/dashboard') # display specific user that is logged in and all the reports that have a matching foreign key to the user id
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }# user is singular because I am getting one (don't need loop to display). reports is plural from get_all so Jinja loop needed in HTML to pick it out.
    return render_template("dashboard.html", user=User.get_by_id(data), reports=Report.get_all_with_user())