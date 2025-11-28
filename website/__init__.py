from flask import Flask, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager, current_user, logout_user
from datetime import timedelta, datetime

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fsdfsadfsafasfasf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_PERMANENT'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    @app.after_request
    def no_cache_pages(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    @app.before_request
    def user_timeout(): # timeout user after a set amount of time
        if not current_user.is_authenticated: # not logged in
            return
        now = datetime.utcnow().timestamp()
        last_activity = session.get('last_activity')
        if last_activity is not None and (now-last_activity>10*60): # user has been afk for 10 minutes
            logout_user()
            session.clear()
            flash('You have been logged out due to inactivity.', 'error')
            return redirect(url_for('auth.login'))
        session['last_activity'] = now


    return app

def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        #db.create_all(app=app)
        db.create_all()
        print('Created Database!')