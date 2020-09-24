import os

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy.exc
import logging

app = Flask(__name__)

engine = create_engine("sqlite:///accountinfo.db")
#btw we have to change this thing ^ everytime we change computers <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["POST"])
def signup():
    return render_template("signup.html")

@app.route('/signup/complete', methods=["POST"])
def signupComplete():
    email = request.form.get("email")
    username = request.form.get("username")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    password = request.form.get("password")
    pswdconfirm = request.form.get('passwordconfirm')

    if password != pswdconfirm:
        return render_template('error.html', message='Please make sure to confirm your password.')

    try: 
        db.execute("INSERT INTO AccountInfo (email, username, firstname, lastname, password) VALUES (:email, :username, :firstname, :lastname, :password)",
        {"email": email, "username": username, "firstname": firstname, "lastname": lastname, "password": password})
    except sqlalchemy.exc.IntegrityError:
        return render_template('error.html', message='Your email address or username is already in use.')
    db.commit()
    return render_template("success.html", message="You successfully signed up!")

@app.route("/login", methods=["POST"])
def login():
    return render_template("login.html")

@app.route("/login/complete", methods=["POST"])
def loginComplete():

    email = request.form.get("email")
    password = request.form.get("password")

    checkEmail = db.execute("SELECT * FROM AccountInfo WHERE email = :email", {"email": email}).fetchone()
    checkPassword = db.execute("SELECT * FROM AccountInfo WHERE password = :password", {"password": password}).fetchone()
    
    if checkEmail != None and checkPassword != None:
        return render_template("success.html", message="You successfully logged in!")
    else:
        return render_template('error.html', message="Invalid Login Credentials")



        




    




