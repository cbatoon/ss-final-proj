from flask import Flask, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_login import LoginManager, current_user, logout_user
from datetime import timedelta, datetime
from flask_wtf import CSRFProtect # anti CSRF tokens

db = SQLAlchemy()
DB_NAME = "database.db"
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Gabriel's Change for "Cookie without SameSite Attribute"
    # --- Secure session cookie settings ---
    # Lax is good for typical login sites; use "Strict" if you don't need cross-site POSTs.
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    # In production over HTTPS, set this to True.
    app.config["SESSION_COOKIE_SECURE"] = False   # True when deployed with HTTPS
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    # End Code

    app.config['SECRET_KEY'] = 'fsdfsadfsafasfasf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_PERMANENT'] = False

    app.config['WTF_CSRF_TIME_LIMIT'] = 600  # 10 minutes
    csrf.init_app(app)

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

    # (Optional) If you really want to keep this separate no-cache handler, you can.
    # But it's redundant because add_CSP_headers also sets Cache-Control.
    # @app.after_request
    # def no_cache_pages(response):
    #     response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    #     response.headers["Pragma"] = "no-cache"
    #     response.headers["Expires"] = "0"
    #     return response

    # Gabriel's Change for CSP Headers security issue
    @app.after_request
    def add_CSP_headers(response):
        # No cache
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        # Security headers
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # CSP (with frame-ancestors and form-action, no unsafe-inline)
        csp = (
            "default-src 'self' https://code.jquery.com https://cdnjs.cloudflare.com "
            "https://stackpath.bootstrapcdn.com https://maxcdn.bootstrapcdn.com; "
            "script-src 'self' https://code.jquery.com https://cdnjs.cloudflare.com; "
            "style-src 'self' https://stackpath.bootstrapcdn.com https://maxcdn.bootstrapcdn.com; "
            "font-src 'self' https://stackpath.bootstrapcdn.com https://maxcdn.bootstrapcdn.com; "
            "img-src 'self' data:; "
            "frame-ancestors 'self'; "
            "form-action 'self';"
        )
        response.headers["Content-Security-Policy"] = csp

        # Hide Werkzeug / Python version
        response.headers.pop("Server", None)

        return response
    # End Code

    @app.before_request
    def user_timeout():  # timeout user after a set amount of time
        if not current_user.is_authenticated:  # not logged in
            return
        now = datetime.utcnow().timestamp()
        last_activity = session.get('last_activity')
        if last_activity is not None and (now - last_activity > 10 * 60):  # user has been afk for 10 minutes
            logout_user()
            session.clear()
            flash('You have been logged out due to inactivity.', 'error')
            return redirect(url_for('auth.login'))
        session['last_activity'] = now

    return app

#End Code


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

        db.create_all()

        print('Created Database!')



