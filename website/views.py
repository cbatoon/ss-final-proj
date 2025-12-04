# stores URL endpoints and view functions
# where users can actually go to...
from . import db
from flask import Blueprint, abort, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from .models import Customer, AuditLogging, User
from werkzeug.security import generate_password_hash
from .logging import log_action

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home(): # homepage
    return render_template("home.html", user=current_user)

@views.route('/clients')
@login_required
def customers():
    all_customers = Customer.query.all()
    return render_template("clients.html", customers=all_customers, user=current_user)

@views.route('/logs')
@login_required
def logs():
    if current_user.role not in ['owner']:
        abort(403) # user authenticated but is not authorized to view page
    all_logs = AuditLogging.query.order_by(AuditLogging.timestamp.desc()).limit(200).all()
    return render_template("logs.html", logs=all_logs, user=current_user)

@views.route('/users')
@login_required
def users():
    if current_user.role not in ("admin", "owner"): # only upper powers can access this
        abort(403)
    all_users = User.query.all()
    return render_template("users.html", users=all_users, user=current_user)




@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')

        current_user.first_name = first_name
        current_user.last_name = last_name

        # Only admin or owner can change email
        if current_user.role in ("admin", "owner"):
            email = request.form.get('email')
            current_user.email = email

        if password:  # update password if provided
            current_user.password = generate_password_hash(password, method='sha256')

        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating profile: {e}", "error")

    return render_template("profile.html", user=current_user)

@views.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    delUser = User.query.get_or_404(id)
    
    if current_user.role not in ("admin", "owner"):
        log_action("unauthorized_delete_action",  f"User {current_user.email} attempted to delete {delUser.email}")
        abort(403) # user authenticated but is not authorized to view page

    try:
        db.session.delete(delUser)
        db.session.commit()
        log_action("delete_user", details=f"Deleted user {delUser.email}")

        flash(f"User {delUser.email} was deleted successfully!")

        all_users = User.query.all()
        return render_template("users.html", users=all_users, user=current_user)
    except Exception as e:
        flash(f"There was an error! {e}")
        log_action("delete_error", details=f"Could not delete User {delUser.email}")

        all_users = User.query.all()
        return render_template("users.html", users=all_users, user=current_user)