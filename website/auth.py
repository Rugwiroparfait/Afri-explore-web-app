from flask import Blueprint, render_template, redirect, url_for, request, flash
import re
import random
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Define a Blueprint for authentication routes
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handle the login functionality.
    
    GET: Renders the login page.
    POST: Authenticates the user and logs them in.
    """
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if a user with the input email exists
        user = User.query.filter_by(email=email).first()

        # Verify the password
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                # If password is incorrect
                flash('Password is incorrect', category='error')
        else:
            flash("Email does not exist", category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    """
    Handle the sign-up functionality.
    
    GET: Renders the sign-up page.
    POST: Registers a new user.
    """
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if user with email or username already exists
        email_exists = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()

        # Regular expression to check if email is valid
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # Validate user input and display appropriate error messages
        if email_exists:
            flash('Email is already in use!', category='error')
        elif username_exist:
            flash('Username already taken', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(username) < 2:
            flash('Username is too short!', category='error')
        elif len(password1) < 6:
            flash('Password is too short', category='error')
        elif not re.match(email_regex, email):
            flash('Email is not valid', category='error')
        else:
            avatar_seed = random.choice(['Bob', 'Ginger', 'Charlie', 'Annie','Buster','Abby'])
            avatar_url = f'https://api.dicebear.com/9.x/adventurer/svg?seed={avatar_seed}'
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'), avatar_url=avatar_url)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    """
    Handle the logout functionality.
    
    Logs out the current user and redirects to the home page.
    """
    logout_user()
    return redirect(url_for("views.home"))
