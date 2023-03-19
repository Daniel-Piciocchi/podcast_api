from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt

# Helper function to check if the user is an admin
def check_admin(claims):
    if not claims.get("is_admin", True):
        raise Exception("You do not have the required permissions")

# Decorator to authenticate a user using JWT
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifies if the request has a valid JWT token
        verify_jwt_in_request()
        # Gets the user's identity (user_id) from the JWT
        user_id = get_jwt_identity()
        return f(user_id, *args, **kwargs)
    return decorated_function

# Decorator to check if the authenticated user is an admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verifies if the request has a valid JWT token
        verify_jwt_in_request()
        # Gets the JWT claims
        jwt_claims = get_jwt()
        print(jwt_claims)
        # Checks if the user has the is_admin claim set to True
        if not jwt_claims.get("is_admin", False):
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper
