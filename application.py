import os

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import logging

app = Flask(__name__)

engine = create_engine("sqlite:///accountinfo.db") #put sqlite database here sqlite:///{file name}
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
    logging.error('%s, %s', username, firstname)
    
    db.execute("INSERT INTO AccountInfo (email, username, firstname, lastname, password) VALUES (:email, :username, :firstname, :lastname, :password)",
     {"email": email, "username": username, "firstname": firstname, "lastname": lastname, "password": password})
    db.commit()
    return "aaa"




    




