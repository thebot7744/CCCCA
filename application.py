import os

from flask import Flask, render_template, request, jsonify, session, flash, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlalchemy.exc
import logging
from flask_session import Session
from flask_socketio import SocketIO

FORMAT =  '%(filename)s:%(funcName)s():L%(lineno)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

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
    loginCheck = False

@app.route('/')
def index():
    global loginCheck
    if session.get('email') is None:
        message = "You are not logged in."
        loginCheck = False
        children = []
        teacher = 0
    else:
        email = session['email']
        loginCheck = True
        message = "You are logged in as " + email

        logging.debug(session)

        sid=session["sid"][0]

        teacher=session["teacher"]

        children = db.execute("SELECT childfirstname, childlastname FROM ChildInfo WHERE parentId = :parentId", {"parentId": sid}).fetchall()

    return render_template('index.html', message=message, children=children, loginCheck=loginCheck, teacher=teacher)

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
    teacher = request.form.get('teacherSignUp')

    data = [email, username, firstname, lastname, password, pswdconfirm]
    for i in data:
        if i == "":
            flash("Make sure to fill in all empty fields.")
            return render_template("signup.html")

    if password != pswdconfirm:
        flash("Make sure to confirm your password.")
        return render_template('signup.html')

    try: 
        db.execute("INSERT INTO AccountInfo (email, username, firstname, lastname, password, teacher) VALUES (:email, :username, :firstname, :lastname, :password, :teacher)",
        {"email": email, "username": username, "firstname": firstname, "lastname": lastname, "password": password, "teacher": teacher})
    except sqlalchemy.exc.IntegrityError:
        flash("Your email address or username is already in use.")
        return render_template('signup.html')
    db.commit()
    session['email'] = email
    sessionId = db.execute("SELECT id FROM AccountInfo WHERE email = :email", {"email": email}).fetchone()
    session["sid"] = sessionId
    session["teacher"] = teacher[0]
    return redirect("/")
    

@app.route("/login", methods=["POST"])
def login():
    return render_template("login.html")

@app.route("/login/complete", methods=["POST"])
def loginComplete():

    email = request.form.get("email")
    password = request.form.get("password")

    check = db.execute("SELECT id, email, password, teacher FROM AccountInfo WHERE email = :email AND password = :password", {"email": email, "password": password}).fetchall()
    logging.debug(check)
    if check != []:
        session['email'] = email
        session["sid"] = check[0][0]
        session["teacher"] = check[0][3]
        logging.debug(session["teacher"])
        return redirect("/")
    else:
        flash("Invalid login credentials.")
        return render_template('login.html')

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
            flash("Make sure to fill in all empty fields.")
            return render_template("child.html")
        

    logging.error(data)
    db.execute("INSERT INTO ChildInfo (childfirstname, childlastname, grade, parentId) VALUES (:childfirstname, :childlastname, :grade, :parentId)",
    {"childfirstname": childfirstname, "childlastname": childlastname, "grade": grade, "parentId": parentId})
    db.commit()
    

    return render_template("success.html", message="You successfully registered a child")

@app.route("/classCreate", methods=["POST"])
def classCreate():
    return render_template("classCreate.html")

@app.route("/classCreate/complete", methods=["POST"])
def classCreateComplete():
    className = request.form.get("className")
    classNum = request.form.get("classNum")
    classGrade = request.form.get("classGrade")
    classDesc = request.form.get("classDesc")
    teacherId = session["sid"]

    data = [className, classNum, classGrade, classDesc]

    for i in data:
        if i=="":
            flash("Make sure to fill in all empty fields.")
            return render_template("classCreate.html")

    logging.debug("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", className, classNum, classGrade, classDesc)

    db.execute("INSERT INTO ClassInfo (className, classNum, classGrade, classDesc, teacherId) VALUES (:className, :classNum, :classGrade, :classDesc, :teacherId)", 
    {"className": className, "classNum": classNum, "classGrade": classGrade, "classDesc": classDesc, "teacherId": teacherId})
    db.commit()

    return render_template("success.html", message="You successfully created a class.")

@app.route("/classes", methods=["POST", "GET"])
def classes():
    classes = db.execute("SELECT * FROM ClassInfo")
    return render_template("classes.html", classes=classes)
