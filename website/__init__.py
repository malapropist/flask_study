# This file makes the website directory a Python package
import os
from os import path
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname, realpath
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    
    # Generate a secure random key or use environment variable
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.static_folder, 'static/book_logo.png', mimetype='image/png')

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .models import User, Note
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        # print('Created Database!')