from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db 

auth = Blueprint('auth', __name__)

#login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # get user by email
        user = User.query.filter_by(email=email).first()
        if user:
            # user exists
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # login user and remember user until he/she clears session
                login_user(user, remember=True)
                return redirect(url_for('views.home', user=user))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', catgory='error')
        
    return render_template('auth/login.html', user=current_user)


# sign up page
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        hashed_password = generate_password_hash(password1, method='sha256')

        if email_exists:
            flash('Email already exists', category='error')
        elif len(email_exists) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif username_exists:
            flash('Username already exists', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(username) < 2:
            flash('Username is too short', category='error')
        elif len(password1) < 7:
            flash('Password mush be at least 7 characters.', category='error')
        # you could verify email here...
        else:
            user = User(email=email, username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            # login user and remember user
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('auth/sign_up.html', user=current_user)

# logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('views.home'))