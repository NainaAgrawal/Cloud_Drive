from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from werkzeug import secure_filename
from datetime import datetime
import pymysql.cursors
import pandas as pd

conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'root',
    database = "cloud"
    )
cursor = conn.cursor()

app = Flask(__name__)

# # Configure sessions
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    if 'user' in session:
        if request.method == "POST":
            download = request.form['download']
            print(download)
        return render_template ("index.html", session=session )
    else:
        if request.method == "POST":
            download = request.form['download']
            print(download)
            return "hello"
    return render_template ( "index.html")

@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/new/", methods=["GET"])
def new():
    # Render log in page
    return render_template("new.html")


@app.route("/logged/", methods=["POST"] )
def logged():
    # Get log in info from log in form
    user = request.form["username"].lower()
    pwd = request.form["password"]
    #pwd = str(sha1(request.form["password"].encode('utf-8')).hexdigest())
    # Make sure form input is not blank and re-render log in page if blank
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    # Find out if info in form matches a record in user database
    rows = pd.read_sql("SELECT * FROM users WHERE username = %s AND password = %s"%('"' + user + '"', '"' + pwd + '"'), con = conn)
    # If username and password match a record in database, set session variables
    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now()
        session['uid'] = int(rows["user_id"][0])
    # Redirect to Home Page
    if 'user' in session:
        return redirect("/" )
    # If username is not in the database return the log in page
    return render_template ( "login.html", msg = "Wrong username or password." )


@app.route("/logout/")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register/", methods=["POST"])
def registration():
    # Get info from form
    username = request.form["username"]
    password = request.form["password"]
    confirm = request.form["confirm"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    phone = request.form["phone"]
    # See if username already in the database
    rows = pd.read_sql("SELECT * FROM users WHERE username = %s"%(('"' + username +'"')), con = conn)
    # If username already exists, alert user
    if len( rows ) > 0:
        return render_template ("new.html", msg = "Username already exists!" )
    # If new user, upload his/her info into the users database
    else:
        cursor.execute( "INSERT INTO users (username, password, fname, lname, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"%('"' + username + '"', '"' + password + '"', '"' + fname + '"', '"' + lname + '"', '"' + email + '"', '"' + phone + '"'))
        # Render login template
        conn.commit()
        return render_template ("login.html" )

@app.route("/share_file/", methods=["GET", "POST"])
def share_file():
    if request.method == "POST":
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join("share_file/" + filename))
        pathh = '/share_file/%s'%(filename)
        print(pathh)
        cursor.execute("INSERT INTO share_file (share_ID, upload_file) VALUES (TO_BASE64(RANDOM_BYTES(3)), LOAD_FILE(%s))"%("'" + pathh + "'"))
        conn.commit()
        secret_id = pd.read_sql("SELECT * FROM share_file", con = conn)
        return str(secret_id["share_ID"].tolist()[-1])
        # return "hello"
    
@app.route("/download_share_file/", methods=["GET", "POST"])
def download_share_file():
    if request.method == "POST":
        download = request.form['download']
        print(download)


if __name__ == '__main__':
	app.run(debug=True)