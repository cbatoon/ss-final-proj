# handles logging in and logging out users

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from .logging import log_action

auth = Blueprint('auth', __name__)

# GET => retrieving information
# POST => some kind of change to website or database


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user)
                log_action("login", details=f"User {user.email} logged in.")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                log_action("failed_login", details=f"Bad password for {email}")
        else:
            flash('Email does not exist.', category='error')
            log_action("failed_login", details=f"Attempted login from unknown email {email}")

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))