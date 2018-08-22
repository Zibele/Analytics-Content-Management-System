from flask import render_template, flash, redirect, url_for, request, Markup
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm, PostForm, CommentForm
from app.models import User, Post, Comment
from app.email import send_password_reset_email
from datetime import datetime
import os

# Timeline page
@app.route("/")
@app.route("/index")
@login_required
def index():
    # Get real posts from db
    page = request.args.get("page", 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config["POSTS_PER_PAGE"], False)
    next_url = url_for("index", page=posts.next_num) \
    if posts.has_next else None
    prev_url = url_for("index", page=posts.prev_num) \
    if posts.has_prev else None
    return render_template("index.html", title="Home" , posts=posts.items, next_url=next_url, prev_url=prev_url)

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
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()

    return render_template("user.html", user=u)

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
@login_required
def add_article():
    form = PostForm()
    if form.validate_on_submit():
        # Create the post
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        post.set_slug(form.title.data)

        # Image handling
        file = form.image.data
        
        # Change the filename
        extension = os.path.splitext(file.filename)[1]
        filename = post.get_slug() + extension

        # Save the file to our file system
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Set the image
        post.set_image(filename)
        
        # Add the post to db
        db.session.add(post)
        db.session.commit()
        flash("You post is now online!")
        return redirect(url_for("index"))

    return render_template("add_article.html", form=form)

# View article
@app.route("/article/<slug>", methods=["GET", "POST"])
def article(slug):
    # Get the current page
    post = Post.query.filter_by(slug=slug).first()

    # Handle comment form handling
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash("You comment is now live")
        return redirect(url_for("article", slug=slug))

    # Handle pagination of comments
    page = request.args.get("page", 1, type=int)
    comments = post.comments.paginate(page, app.config["POSTS_PER_PAGE"], False)
    next_url = url_for("article", slug=slug, page=comments.next_num) \
    if comments.has_next else None
    prev_url = url_for("article", slug=slug, page=comments.prev_num) \
    if comments.has_prev else None

    # Wrap the content as HTML
    body = Markup(post.body)

    return render_template("article.html", title=post.title, body=body, post=post, comments=comments.items, next_url=next_url, prev_url=prev_url, form=form)



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


        