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
        avatar_url (str): URL for avatars' APIs.
        comments (list[Comment]): Relationship to the Comment model, representing the user's comments.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    avatar_url = db.Column(db.String(300))
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    
class Post(db.Model):
    """
    Post model to store post details.

    Attributes:
        id (int): Primary key for the post.
        text (str): Content of the post.
        date_created (datetime): The date and time when the post was created.
        author (int): Foreign key to the User model, representing the post's author.
        comments (list[Comment]): Relationship to the Comment model, representing the post's comments.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
class Comment(db.Model):
    """
    Comment model to store comment details.

    Attributes:
        id (int): Primary key for the comment.
        text (str): Content of the comment.
        date_created (datetime): The date and time when the comment was created.
        author (int): Foreign key to the User model, representing the comment's author.
        post_id (int): Foreign key to the Post model, representing the post the comment belongs to.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
