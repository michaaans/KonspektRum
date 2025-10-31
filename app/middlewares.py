
from functools import wraps
from flask_login import current_user
from flask import abort


def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role.name != role_name:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def teacher_required(f):
    return role_required('teacher')(f)


def admin_required(f):
    return role_required('admin')(f)