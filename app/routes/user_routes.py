from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import User, UserSchema
from app.utils import authenticate, admin_required

user_bp = Blueprint("user_bp", __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Register a new user
@user_bp.route('/api/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False)  # Add this line

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = User.query.filter(User.username == username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username, email=email, is_admin=is_admin)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# Login an existing user
@user_bp.route('/api/users/login', methods=['POST'])
def login_user():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return make_response(jsonify({"message": "Missing username or password"}), 400)

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.is_admin})
        return make_response(jsonify({"access_token": access_token}), 200)
    else:
        return make_response(jsonify({"message": "Invalid username or password"}), 401)


# Get all users
@user_bp.route('/api/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    result = users_schema.dump(users)
    return make_response(jsonify(result), 200)

# Get a specific user
@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id, description="There is no user with that ID")
    result = user_schema.dump(user)
    return make_response(jsonify(result), 200)


# Get the current user's profile
@user_bp.route('/api/users/profile', methods=['GET'])
@authenticate
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_admin': user.is_admin
    }

    return jsonify({"user": user_data}), 200

# Update the current user's profile
@user_bp.route('/api/users/profile', methods=['PUT'])
@authenticate
def update_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return make_response(jsonify({"message": "User not found"}), 404)

    data = request.get_json()

    username = data.get('username', None)
    email = data.get('email', None)

    if username:
        user.username = username
    
    if email:
        user.email = email

    db.session.commit()

    return make_response(jsonify({"message": "User profile updated successfully"}), 200)

# Delete the current user
@user_bp.route('/api/users/delete', methods=['DELETE'])
@authenticate
def delete_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return make_response(jsonify({"message": "User not found"}), 404)

    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify({"message": "User deleted successfully"}), 200)

