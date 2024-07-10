from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    """
    User model to store user details.

    Attributes:
        id (int): Primary key for the user.
        email (str): Unique email address of the user.
        username (str): Unique username of the user.
        password (str): Hashed password of the user.
        date_created (datetime): The date and time when the user was created.
        posts (list[Post]): Relationship to the Post model, representing the user's posts.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    avatar_url = db.Column(db.String(200)) 


class Post(db.Model):
    """
    Post model to store post details.

    Attributes:
        id (int): Primary key for the post.
        text (str): Content of the post.
        date_created (datetime): The date and time when the post was created.
        author (int): Foreign key to the User model, representing the post's author.
    """

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
