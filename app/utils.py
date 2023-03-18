from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def check_admin(claims):
    if not claims.get("is_admin", False):
        raise Exception("You do not have the required permissions")

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        return f(*args, **kwargs)
    return decorated_function

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        jwt_claims = get_jwt()
        if not jwt_claims.get("is_admin", False):  # Check for the is_admin claim
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper
