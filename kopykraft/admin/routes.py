from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from kopykraft.extensions import db
from webforms import UserForm
from kopykraft.models import Users, Posts
from kopykraft.admin import admin

# admin dashboard
@admin.route('/')
@login_required
def dashboard():
    if current_user.id == 13:
        return render_template('admin/dashboard.html')
    else:
        flash('Sorry you must be Admin to access this page')
        return redirect(url_for('dashboard'))

# add new user
@admin.route('/users/create', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    # validate form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # hash password
            hashed_password = generate_password_hash(form.password_hash.data, "sha256")
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
    return render_template('admin/users/add.html', form=form, name=name, users=users)

# update user details
@admin.route('/users/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    form = UserForm()
    user = Users.query.get_or_404(id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.username = request.form['username']
        user.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template('admin/users/update.html', form=form, user=user, id=id)
        except:
            flash('Error! Looks like there was a problem....try again!')
            return render_template('admin/users/update.html', form=form, user=user, id=id)
    else:
        return render_template('admin/users/update.html', form=form, user=user, id=id)
    
# delete user
@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    # check if user is an admin
    if current_user.id == 13:
        user = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user)
            db.session.commit()
            flash('User Deleted Successfully!')
            users = Users.query.order_by(Users.date_added)
            return render_template('admin/users/add.html', form=form, name=name, users=users, id=id)
        except:
            flash('Whoops! There was a problem deleting the user....try again.')
            return render_template('admin/users/add.html', form=form, name=name, users=users, id=id)
    else:
        flash('Sorry, you are not authorized to delete that user')
        return redirect(url_for('admin.dashboard'))
    
    