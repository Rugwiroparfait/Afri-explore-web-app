from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user ,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
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

@views.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Dashboard view for the user to update their profile information.

    This route handles both GET and POST requests. On a GET request, it renders the dashboard 
    template with the current user's information. On a POST request, it updates the user's 
    information based on the form input and commits the changes to the database.

    Methods:
        GET: Renders the dashboard template.
        POST: Updates the user's profile information.

    Returns:
        Rendered template for the dashboard.
    """
    if request.method == 'POST':
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        new_avatar = request.form.get('avatar')

        if new_username:
            current_user.username = new_username
        if new_email:
            current_user.email = new_email
        if new_password:
            current_user.password = generate_password_hash(new_password, method='sha256')
        if new_avatar:
            current_user.avatar_url = new_avatar

        db.session.commit()
        flash('Account updated successfully', category='success')

    return render_template("dashboard.html", user=current_user)

@views.route("/delete-account", methods=['POST'])
@login_required
def delete_account():
    """
    Route to delete the current user's account.

    This route handles the deletion of the user's account, including all posts, comments, 
    and likes associated with the user. It logs out the user and redirects them to the login 
    page upon successful deletion.

    Methods:
        POST: Deletes the user's account and associated data.

    Returns:
        Redirects to the login page upon successful deletion.
        Renders the dashboard template with an error message upon failure.
    """
    user = User.query.filter_by(id=current_user.id).first()
    if user:
        # Delete all posts, comments, and likes associated with the user
        posts = Post.query.filter_by(author=user.id).all()
        for post in posts:
            comments = Comment.query.filter_by(post_id=post.id).all()
            for comment in comments:
                db.session.delete(comment)
            likes = Like.query.filter_by(post_id=post.id).all()
            for like in likes:
                db.session.delete(like)
            db.session.delete(post)
        
        # Delete comments and likes that the user has made
        comments = Comment.query.filter_by(author=user.id).all()
        for comment in comments:
            db.session.delete(comment)
        likes = Like.query.filter_by(author=user.id).all()
        for like in likes:
            db.session.delete(like)

        # Delete the user
        db.session.delete(user)
        db.session.commit()
        logout_user()
        flash('Account deleted successfully', category='success')
        return redirect(url_for('auth.login'))

    flash('Account deletion failed', category='error')
    return redirect(url_for('views.dashboard'))


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

@views.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Handle the editing of a post.

    Args:
        post_id (int): The ID of the post to be edited.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user.id:
        flash('You do not have permission to edit this post', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post.text = text
            db.session.commit()
            flash('Post updated', category='success')
            return redirect(url_for('views.home'))

    return render_template('edit_post.html', user=current_user, post=post)

