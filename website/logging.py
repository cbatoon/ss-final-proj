from flask_login import current_user
from . import db
from .models import AuditLogging

def log_action(action, details=None):
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None  # unknown user

    log = AuditLogging(
        user_id=user_id,
        action=action,
        details=details
    )
    db.session.add(log)
    db.session.commit()