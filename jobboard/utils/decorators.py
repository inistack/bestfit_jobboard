from functools import wraps
from flask_smorest import abort
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(role):
    """Decorator requires user role for access to a route."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('role') != role:
                abort(403, message=f"{role.capitalize()} role required")
            return fn(*args, **kwargs)
        return wrapper
    return decorator