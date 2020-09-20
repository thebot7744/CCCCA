import os

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy.exc
import logging

app = Flask(__name__)

engine = create_engine("sqlite:////Users/christopherwang/PycharmProjects/CCCCA/CCCCA/accountinfo.db") #put sqlite database here sqlite:///{file name}
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods = ["POST"])
def signup():

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
        return render_template('error.html', message='Your email address is already in use.')
    db.commit()
    return render_template("success.html")


        




    




