# This file makes the website directory a Python package
import os
from os import path
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname, realpath
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime

db = SQLAlchemy()
DB_NAME = "database.db"

scheduler = APScheduler()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri = f'memory://localhost:5000'
)

def create_app():
    app = Flask(__name__)
    
    # Generate a secure random key or use environment variable
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    limiter.init_app(app)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(app.static_folder, 'static/book_logo.png', mimetype='image/png')

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    from .models import User, Note, Group, UserGroupsAssociation
    
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    scheduler.init_app(app)
    scheduler.add_job(id='reset_weekly_scores',
                     func=lambda: reset_weekly_scores(app),
                     trigger='cron',
                     day_of_week='sun',
                     hour=0,
                     minute=0)  # Run every Sunday at midnight
    scheduler.start()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()

def reset_weekly_scores(app):
    from .models import User, Note, Group, UserGroupsAssociation
    print("resetting weekly scores")
    with app.app_context():
        try:
            User.query.update({User.weekly_score: 0})
            db.session.commit()
            print(f"Weekly scores reset at {datetime.now()}")
        except Exception as e:
            db.session.rollback()
            print(f"Error resetting scores: {e}")