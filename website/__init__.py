from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from .models import db, DB_NAME, User
from .views import views # relative import
from .auth import auth 

def create_app():
    # Init app
    app = Flask(__name__)
    # configure secret key
    app.config['SECRET_KEY'] = 'flskblggr23'
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # setup database if it doesn't exist
    with app.app_context():
        db.create_all()

    # register blueprints
    app.register_blueprint(auth, url_prefix="")
    app.register_blueprint(views, url_prefix="")

    # set up flask login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# def create_database(app):
    # if not path.exists('website/' + DB_NAME):
    #     db.create_all(app)
    #     print("Created database!")
    