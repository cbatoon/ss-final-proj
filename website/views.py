# stores URL endpoints and view functions
# where users can actually go to...
from . import db
from flask import Blueprint, abort, render_template, flash
from flask_login import current_user, login_required
from .models import Customer, AuditLogging, User
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

#New function for deleting users
@views.route('/delete/<int:id>')
@login_required
def delete(id):
    delUser = User.query.get_or_404(id)
    
    if current_user.role not in ("admin", "owner"):
        abort(403) # user authenticated but is not authorized to view page

    try:
        db.session.delete(delUser)
        db.session.commit()
        flash(f"User {delUser} was deleted successfully!")

        all_users = User.query.all()
        return render_template("users.html", users=all_users, user=current_user)
    except Exception as e:
        flash(f"There was an error! {e}")
        all_users = User.query.all()
        return render_template("users.html", users=all_users, user=current_user)