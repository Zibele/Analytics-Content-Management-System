from flask import render_template
from app import app
from app.forms import LoginForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    
        