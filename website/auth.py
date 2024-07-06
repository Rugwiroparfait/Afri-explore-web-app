from flask import Blueprint, render_template, redirect, url_for, request, flash
import re
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash,check_password_hash


auth = Blueprint("auth", __name__)





@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        #check if user of the input email exist

        user = User.query.filter_by(email=email).first()

        #check if password is correct
        if user:
           if check_password_hash(user.password, password):
               flash("Logged in!", category="success")
               login_user(user, remember=True)
               return redirect(url_for('views.home'))
           
           else:
               #if password is incorrect
               flash('Password is incorrect', category='error')
        else:
            flash("Email does not exist", category='error')

    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #checking if user exists or not
        
        email_exists = User.query.filter_by(email=email).first()
        username_exist =User.query.filter_by(username=username).first()

        #regular expression to check if email is valid

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


        #possible errors that User can make in logging in check
        #to avoid that we can get in invalid information

        if email_exists:
            flash('email is already in use!', category='error')
        elif username_exist:
            flash('username already taken', category='error')
        elif password1 != password2:
            flash('password doesn\'t match', category='error')
        elif len(username) < 2:
            flash('Username is too short!', category='error')
        elif len(password1) < 6:
            flash('password is too short', category='error')
        elif not re.match(email_regex, email):
            flash('email not valid', category='error')

        else:
            #create a new user
            new_user = User(email=email, username=username, password= generate_password_hash(password1, method= 'pbkdf2:sha256'))

            #add the new user in a database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User Created')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))