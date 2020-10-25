import os

from flask import Flask, render_template, request, jsonify, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy.exc
import logging
from flask_session import Session
from flask_socketio import SocketIO


app = Flask(__name__)

engine = create_engine("sqlite:///accountinfo.db")
#btw we have to change this thing ^ everytime we change computers <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
db = scoped_session(sessionmaker(bind=engine))

app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = "very secret oh yes no one will ever guess this"

socketio = SocketIO(app)
socketio.run(app)

@socketio.on('disconnect')
def on_disconnect():
    global loginCheck
    loginCheck=False

@app.route('/')
def index():
    global loginCheck
    if session.get('email') is None:
        message = "You are not signed in."
        loginCheck = False
        children = []
    else:
        email = session['email']
        loginCheck = True
        message = "You are signed in as " + email
        parentId=session["sid"]
        children = db.execute("SELECT childfirstname, childlastname FROM ChildInfo WHERE parentId = :parentId", {"parentId": parentId}).fetchall()


    return render_template('index.html', message=message, children=children, loginCheck=loginCheck)

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('email', None)
    return render_template("success.html", message="You successfully signed out!")

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

    data = [email, username, firstname, lastname, password, pswdconfirm]
    for i in data:
        if i == "":
            return render_template("error.html", message="Make sure to fill in all empty fields.")

    if password != pswdconfirm:
        return render_template('error.html', message='Please make sure to confirm your password.')

    try: 
        db.execute("INSERT INTO AccountInfo (email, username, firstname, lastname, password) VALUES (:email, :username, :firstname, :lastname, :password)",
        {"email": email, "username": username, "firstname": firstname, "lastname": lastname, "password": password})
    except sqlalchemy.exc.IntegrityError:
        return render_template('error.html', message='Your email address or username is already in use.')
    db.commit()
    session['email'] = email
    sessionId = db.execute("SELECT id FROM AccountInfo WHERE email = :email", {"email": email}).fetchone()
    session["sid"] = sessionId
    return render_template("success.html", message="You successfully signed up!")
    

@app.route("/login", methods=["POST"])
def login():
    return render_template("login.html")

@app.route("/login/complete", methods=["POST"])
def loginComplete():

    email = request.form.get("email")
    password = request.form.get("password")

    check = db.execute("SELECT id, email, password FROM AccountInfo WHERE email = :email AND password = :password", {"email": email, "password": password}).fetchall()

    if check != None:
        session['email'] = email
        session["sid"] = check[0][0]
        logging.error(check)
        return render_template("success.html", message="You successfully logged in!")
    else:
        return render_template('error.html', message="Invalid Login Credentials")

@app.route("/child", methods=["POST"])
def child():
    return render_template("child.html")

@app.route("/child/complete", methods=["POST"])
def childComplete():
    childfirstname = request.form.get("childfirstname")
    childlastname = request.form.get('childlastname')
    grade = request.form.get("grade")
    parentId = session["sid"]
    logging.error(parentId)

    data = [childfirstname, childlastname, grade]
    for i in data:
        if i == "":
            return render_template("error.html", message="Make sure to fill in all empty fields.")

    logging.error(data)
    db.execute("INSERT INTO ChildInfo (childfirstname, childlastname, grade, parentId) VALUES (:childfirstname, :childlastname, :grade, :parentId)",
    {"childfirstname": childfirstname, "childlastname": childlastname, "grade": grade, "parentId": parentId})
    db.commit()
    

    return render_template("success.html", message="You successfully registered a child!")