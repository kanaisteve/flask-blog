from kopykraft.extensions import db, migrate, ckeditor
from flask import Flask, render_template
from config import Config
from flask_login import LoginManager
from kopykraft.models import Users
from kopykraft.auth import auth
from kopykraft.home import home
from kopykraft.profile import profile
from kopykraft.admin import admin
from kopykraft.posts import posts
from kopykraft.user import user
from webforms import SearchForm

def create_app(config_class=Config):
    # Init app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize db
    db.init_app(app)
    # Initialize flask-migrate
    migrate.init_app(app, db)
    # Initialize ckeditor
    ckeditor.init_app(app)

    # Configure Flask Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    # login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
    
    # Register blueprints here
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(posts, url_prefix='/posts')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(profile, url_prefix='/profile')

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
    
    # setup database if it doesn't exist
    with app.app_context():
        db.create_all()

    return app