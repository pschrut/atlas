from functools import wraps
from flask import abort
from flask_login import current_user
from app.enums import Roles

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role_id != Roles.ADMIN.value:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
