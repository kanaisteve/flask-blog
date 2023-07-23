from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, request
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, logout_user, LoginManager, login_required, login_user, current_user
from webforms import UserForm, LoginForm, NamerForm, PostForm, SearchForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os

# Init app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'k2494tech'

# Add Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password22@localhost/flskr_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Init db
db = SQLAlchemy(app)
migrate = Migrate(app, db) # migrates our app with our database

ckeditor = CKEditor(app)

# Configure Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create User Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(200))
    about = db.Column(db.Text(), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    password_hash = db.Column(db.String(128), nullable=False)
    # user can have many posts
    posts = db.relationship('Posts', backref='author', passive_deletes=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create a String
    def __repr__(self):
        return '<Name %r>' % self.name
    
# Create Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))
    # foreign key to link user (refer to primary key of the user)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)


# setup database if it doesn't exist
with app.app_context():
    db.create_all()

# home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', current_user=current_user)

# about page
@app.route('/about')
def about():
    return render_template('about.html', current_user=current_user)

# services page
@app.route('/services')
def services():
    return render_template('services.html', current_user=current_user)

# create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash('Form Submited Successfully!')

    return render_template('profile/name.html',name=name, form=form)

# login test page
@app.route('/login-test', methods=['GET', 'POST'])
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

# create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check password hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Successfully!')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password - Try Again!')
        else:
            flash('That user does not exist. Try again...')

    return render_template('auth/login.html', form=form)

# create logout route
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out! Thanks for stopping by...')
    return redirect(url_for('login'))


# create dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
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
        if request.files['profile_pic']:
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
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
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

    return render_template('dashboard.html')

# create admin page
@app.route('/admin')
@login_required
def admin():
    if current_user.id == 13:
        return render_template('admin/dashboard.html')
    else:
        flash('Sorry you must be Admin to access this page')
        return redirect(url_for('dashboard'))

# add new user
@app.route('/user/add', methods=['GET', 'POST'])
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
    return render_template('users/add.html', form=form, name=name, users=users)

# update user
@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
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
            return render_template('users/update.html', form=form, user=user, id=id)
        except:
            flash('Error! Looks like there was a problem....try again!')
            return render_template('users/update.html', form=form, user=user, id=id)
    else:
        return render_template('users/update.html', form=form, user=user, id=id)
    
# delete user
@app.route('/user/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
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
        return redirect(url_for('dashboard'))

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        # get data from form
        title = form.title.data
        content = form.content.data
        slug = form.slug.data
        author_id = current_user.id

        # create new post
        post = Posts(title=title, content=content, slug=slug, author_id=author_id)

        # clear form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''

        # Add post data to db
        db.session.add(post)
        db.session.commit()

        # Return a flash message
        flash("Blog Post Submitted Sucessfully!")
        return redirect(url_for('posts'))
    
    # Return to the webpage
    return render_template("posts/create.html", form=form)

# Get All Blog Posts
@app.route('/posts')
def posts():
    # fetch all posts from database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts/index.html', posts=posts)

# Get Single Blog Post
@app.route('/posts/<int:id>')
def post(id):
    # fetch all posts from database
    post = Posts.query.get_or_404(id)
    return render_template('posts/post.html', post=post)

# Edit Blog Post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()

    # handle post update
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        author_id = current_user.id

        # update database
        db.session.add(post)
        db.session.commit()
        flash('Post Update Successfully!')
        return redirect(url_for('post', id=id))
    
    # check if current user is the author or admin(id:13) of the post
    if current_user.id == post.author.id or current_user.id == 13:
        form.title.data = post.title
        form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('posts/edit.html', post=post, form=form)
    else:
        flash('You are\'t authorized to edit this post...')
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts/index.html', posts=posts)


# Delete Blog Post
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    user_id = current_user.id

    # get all post from database
    posts = Posts.query.order_by(Posts.date_posted)

    # only allow author or admin(id:13) of post to delete this post
    if user_id == post.author.id or id == 13:
        try:
            db.session.delete(post)
            db.session.commit()
            # return message
            flash('Blog Post Delete Successfully!')
            # get all post from database
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts/index.html', posts=posts)
        except:
            # return error message
            flash('Whoops! There was a problem when deleting the blog post, try again...')
            return redirect(url_for('posts', posts=posts))
    else:
        # flash message to user
        flash('You Aren\'t Authorized to delete that post')
        return redirect(url_for('posts'))
    
# create search function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query

    if form.validate_on_submit():
        search = form.search.data
        # query the database
        posts = posts.filter(Posts.content.like('%' + search + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template('posts/search_result.html', form=form, search=search, posts=posts)
    
# pass stuff to navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)
        
# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# return json data
@app.route('/date')
def get_current_date():
    return {"Date": date.today()}

@app.route('/engineers')
def get_engineers():
    engineers = {
        "Kanai": "Frontend Engineer",
        "Peter": "Backend Engineer",
        "Katumbi": "Software Engineer",
        "Victor": "Cybersecurity",
    }

    return engineers
    


# Run Server
if __name__ == '__main__':
    app.run(debug=True, port=2025)