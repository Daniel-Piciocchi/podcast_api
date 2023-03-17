from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def check_admin(claims):
    if not claims.get("is_admin", False):
        raise Exception("You do not have the required permissions")

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        return f(*args, **kwargs)
    return decorated_function

def authenticate_and_authorize_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_identity()
        check_admin(claims)
        return f(*args, **kwargs)
    return decorated_function
