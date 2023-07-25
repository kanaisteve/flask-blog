from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from webforms import LoginForm, UserForm
from kopykraft.extensions import db
from kopykraft.models import Users
from kopykraft.auth import auth

# register user
@auth.route('/register', methods=['GET', 'POST'])
def register():
    name = None
    form = UserForm()
    # validate form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # hash password
            hashed_password = generate_password_hash(form.password_hash.data, "scrypt")
            print(hashed_password)
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        # clear the form
        form.name.data = '' 
        form.username.data = '' 
        form.email.data = '' 
        form.favorite_color.data = '' 
        form.password_hash.data = ''
        flash('User Added Successfully!')

    users = Users.query.order_by(Users.date_added)
    return render_template('auth/register.html', form=form, name=name, users=users)

# create login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check password hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Successfully!')
                return redirect(url_for('user.dashboard'))
            else:
                flash('Wrong password - Try Again!')
        else:
            flash('That user does not exist. Try again...')

    return render_template('auth/login.html', form=form)

# create logout route
@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out! Thanks for stopping by...')
    return redirect(url_for('auth.login'))

# login test page
@auth.route('/login-test', methods=['GET', 'POST'])
def login_test():
    email = None
    password = None
    user = None
    password = None
    form = LoginForm()

    # validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        # clear form
        form.name.data = ''
        form.password = ''

        user = Users.query.filter_by(email=email).first()

        # check hashed password (returns true or false)
        passed = check_password_hash(user.password.hash, password)

        flash('You have logged in successfully!')

    return render_template('auth/signin.html', email=email, password=password, form=form, user=user, passed=passed)
