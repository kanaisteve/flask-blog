from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from kopykraft.profile import profile
from webforms import NamerForm, UserForm
from kopykraft.models import Users
from kopykraft.extensions import db


# update user details
@profile.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
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
            return render_template('profile/update.html', form=form, user=user, id=id)
        except:
            flash('Error! Looks like there was a problem....try again!')
            return render_template('profile/update.html', form=form, user=user, id=id)
    else:
        return render_template('profile/update.html', form=form, user=user, id=id)
    

# delete account
@profile.route('/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    # check if user is owner of account
    if id == current_user.id:
        user = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user)
            db.session.commit()
            flash('User Deleted Successfully!')
            users = Users.query.order_by(Users.date_added)
            return render_template('users/add.html', form=form, name=name, users=users, id=id)
        except:
            flash('Whoops! There was a problem deleting the user....try again.')
            return render_template('users/add.html', form=form, name=name, users=users, id=id)
    else:
        flash('Sorry, you are not authorized to delete that user')
        return redirect(url_for('user.dashboard'))
    
# create name page
@profile.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submited Successfully!')

    return render_template('profile/name.html',name=name, form=form)