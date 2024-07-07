from flask import Blueprint, render_template, request, redirect,flash, url_for
from flask_login import login_required, current_user
from . import db
from .models import Post

views = Blueprint("views", __name__)




@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/make-post", methods=['GET', 'POST'])
@login_required
def make_post():
    if request.method == 'POST':
        text = request.form.get('text')
        
        if not text:
            flash('You must write something', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created', category='success')
            return redirect(url_for('views.home'))
    return render_template('make_post.html' ,user=current_user)