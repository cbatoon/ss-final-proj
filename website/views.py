# stores URL endpoints and view functions
# where users can actually go to...
from flask import Blueprint, render_template
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