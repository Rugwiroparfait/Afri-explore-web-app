from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from . import db
from .models import Post, User, Comment, Like

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
    if post.author != current_user.id:
        flash('You do not have permission to delete this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')
    return redirect(url_for('views.home'))


@views.route("posts/<username>")
@login_required
def posts(username):
    """
    Handle the user's posts, one user profile.

    Args:
        username (str): The username of the user whose posts are to be displayed.
    """
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that name exists', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("post.html", user=current_user, posts=posts, username=username)


@views.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment(post_id):
    """
    Handle the submission of a comment.

    Args:
        post_id (int): The ID of the post to comment on.

    Returns:
        Redirects to the post view with the new comment.
    """
    text = request.form.get('text')
    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        new_comment = comment(text=text, author=current_user.id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added.', category='success')

    return redirect(url_for('views.posts', username=current_user.username))

@views.route("/add_comment/<post_id>", methods=["POST"])
@login_required
def add_comment(post_id):
    text = request.form.get("text")

    if not text:
        flash("Comment cannot be empty", category="error")
    else:
        post = Post.query.get(post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment added!", category="success")
        else:
            flash("Post not found", category="error")

    return redirect(url_for("views.home"))

@views.route("/delete_comment/<comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        if comment.user.id == current_user.id:
            db.session.delete(comment)
            db.session.commit()
            flash("Comment deleted!", category="success")
        else:
            flash("You do not have permission to delete this comment", category="error")
    else:
        flash("Comment not found", category="error")
    
    return redirect(url_for("views.home"))


@views.route('/like-post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        like = Like.query.filter_by(post_id=post_id, author=current_user.id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return "Unliked", 200
        else:
            new_like = Like(post_id=post_id, author=current_user.id)
            db.session.add(new_like)
            db.session.commit()
            return "Liked", 200
    return "Post not found", 404
