from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post
from app.email import send_password_reset_email
from datetime import datetime

# Timeline page
@app.route("/")
@app.route("/index")
@login_required
def index():
    """ Display the user timeline"""
    return render_template("index.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    # Check if user is logged in already
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    # Instantiate a login object from LoginForm class
    form = LoginForm()
    
    # Process user-submitted data from form
    if form.validate_on_submit():
        # Get user from database
        user = User.query.filter_by(username=form.username.data).first()

        # Validate user input from form
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        
        # Login the user and remember the user
        login_user(user, remember=form.remember_me.data)

        # Redirect after logging in
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")

        return redirect(next_page)
    # Render template
    return render_template("login.html", title="Sign In", form=form)

    
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    
    return render_template("register.html", title="Register", form=form)

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


        