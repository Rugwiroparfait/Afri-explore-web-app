from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from . import db
from .models import Post

# Define a Blueprint for view routes
views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    """
    Render the home page with all posts.
    
    This view requires the user to be logged in.
    """
    # Query all posts from the database
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/make-post", methods=['GET', 'POST'])
@login_required
def make_post():
    """
    Handle the creation of a new post.
    
    GET: Renders the make post page.
    POST: Creates a new post and adds it to the database.
    """
    if request.method == 'POST':
        text = request.form.get('text')

        # Validate the post text
        if not text:
            flash('You must write something', category='error')
        else:
            # Create a new post
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created', category='success')
            return redirect(url_for('views.home'))
    
    return render_template('make_post.html', user=current_user)


@views.route("/delete-post/<int:post_id>", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Handle the deletion of a post.
    
    Args:
        post_id (int): The ID of the post to be deleted.
    """
    post = Post.query.get_or_404(post_id)
    
    if post.user.id != current_user.id:
        flash("You do not have permission to delete this post", category="error")
        return redirect(url_for('views.home'))
    
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted", category="success")
    return redirect(url_for('views.home'))
