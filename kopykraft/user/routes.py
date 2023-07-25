from flask import render_template, flash, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from kopykraft.extensions import db
from werkzeug.utils import secure_filename
from kopykraft.user import user
from kopykraft.models import Users
from webforms import UserForm
import uuid as uuid
import os

# create dashboard page
@user.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    user = Users.query.get_or_404(id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.username = request.form['username']
        user.favorite_color = request.form['favorite_color']
        user.about = request.form['about']

        # check if avatar was submitted
        if request.files['avatar']:
            user.avatar = request.files['avatar']
            # grab image name
            filename = secure_filename(user.avatar.filename)
            unique_filename = str(uuid.uuid1()) + "_" + filename
            # Save image to folder path
            # user.avatar.save(os.path.join(app.config['UPLOAD_FOLDER']), unique_filename)
            saver = request.files['avatar']
            # change it to a string to save to db
            user.avatar = unique_filename

            try:
                db.session.commit()
                saver.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), unique_filename))
                flash('User Updated Successfully!')
                return render_template('dashboard.html', form=form, user=user, id=id)
            except:
                flash('Error! Looks like there was a problem....try again!')
                return render_template('dashboard.html', form=form, user=user, id=id)
        else:
            db.session.commit()
            flash('User Updated Successfully!')
            return render_template('dashboard.html', form=form, user=user, id=id)
    else:
        return render_template('dashboard.html', form=form, user=user, id=id)