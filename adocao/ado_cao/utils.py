from flask import abort
from flask_login import current_user

def admin_required():
    if not current_user.is_authenticated or not current_user.has_role("admin"):
        abort(403)
