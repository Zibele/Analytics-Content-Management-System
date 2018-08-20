from app import db
from app import login
from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
from slugify import slugify
import jwt
from app import app

# Followers association table
followers = db.Table("followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id"))
    )

# Users database table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    comments = db.relationship("Comment", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many follow relationship
    followed = db.relationship(
        "User", 
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"), 
        lazy="dynamic"
    )


    # Print an object the of class for debugging purposes
    def __repr__(self):
        return f"<User {self.username}>"
    
    # Hash the user password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Compare original password and hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Return the URL for user avatar's image
    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    # Follow another user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    # Stop following a user
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # Determine if user is following another user
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    # Query the db for posts of followed users, with user's own posts
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
    # JWT Password reset methods
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({"reset_password": self.id, "exp": time()+ expires_in}, app.config["SECRET_KEY"], algorithm='HS256').decode("utf-8")
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
# Register function as user loader
@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    image = db.Column(db.Text)
    slug = db.Column(db.Text, index=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship("Comment", backref="post", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Post {self.body}>"
    
    def set_slug(self, title):
        self.slug = slugify(title)
    
    def get_slug(self):
        return self.slug
    
    def set_image(self, filename):
        image = filename
        

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr(self):
        return f"<Comment {self.body}>"



