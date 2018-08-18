from flask import render_template, url_for
from app import app
from app.forms import LoginForm

# Timeline page
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

@app.route("/logout")
def logout():
    """Log the user out"""
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user"""

# Profile page
@app.route("/user/<username>")
def user(username):
    """Display profile page"""

# Edit profile page
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    """Edit profile"""

@app.route("/follow/<username>")
def follow(username):
    """Follow user"""

@app.route("/unfollow/<username>")
def unfollow(username):
    """Unfollow user"""

@app.route("/explore")
def explore():
    """ Show all posts"""

@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    """Request password change"""

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """ Change password"""

# Add article
@app.route("/add_article", methods=["GET", "POST"])
def add_article():
    """Add article"""

# View article
@app.route("/article/<title>", methods=["GET", "POST"])
def article(title):
    """ View individual article"""

# Edit article
@app.route("/edit_article", methods=["GET", "POST"])
def edit_article():
    """Edit article"""

# Dashboard
@app.route("/dashboard")
def dashboard():
    """ Show dashboard"""

# Record time of last visit for user
@app.before_request
def before_request():
    """Record last time user was on site"""


        