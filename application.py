import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Set up application
class User:
    def __init__(self, userId, userName, userPass):
        self.id = userId
        self.name = userName
        self.password = userPass


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loggedin", methods=["POST"])
def loggedin():
    username = request.form.get("name")
    userpass = request.form.get("password")
# checking if user exists and if exists check if password is matched
    matchuser = db.execute("select userid, username, userpass from userinfo where username = :username", {"username": username}).fetchone()
#    print (f"{matchuser.userpass}")

    if matchuser.userpass == userpass:
        return render_template("loggedin.html", name=username, password=userpass)
    else:
        return render_template("index.html")

#    return render_template("loggedin.html", name=name, password=password)
