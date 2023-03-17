from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import User, UserSchema
from app.utils import check_admin

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

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the user already exists in the database
    existing_user = User.query.filter(User.username == username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # Create a new user and add it to the database
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    new_user.role = 'user'

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

    # Check if the user exists in the database and the password is correct
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(
            identity=user.id, additional_claims={"role": user.role})
        return make_response(jsonify({"access_token": access_token}), 200)
    else:
        return make_response(jsonify({"message": "Invalid username or password"}), 401)

# Get all users


@user_bp.route('/api/users', methods=['GET'])
@jwt_required()
def get_all_users():
    if not check_admin():
        return make_response(jsonify({"message": "Unauthorized"}), 403)

    # Query the database for all User records
    users = User.query.all()
    result = users_schema.dump(users)
    return make_response(jsonify(result), 200)

# Get a specific user


@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    if not check_admin():
        return make_response(jsonify({"message": "Unauthorized"}), 403)

    # Query the database for a specific User record by its ID
    user = User.query.get_or_404(user_id)
    result = user_schema.dump(user)
    return make_response(jsonify(result), 200)

# Get the current user's profile


@user_bp.route('/api/users/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    # Query the database for the User record by its ID
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }

    return jsonify({"user": user_data}), 200

# Update the current user's profile


@user_bp.route('/api/users/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    current_user_id = get_jwt_identity()
    # Query the database for the User record by its ID
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

    # Update the user record in the database
    db.session.commit()

    return make_response(jsonify({"message": "User profile updated successfully"}), 200)

# Delete the current user


@user_bp.route('/api/users/delete', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()
    # Query the database for the User record by its ID
    user = User.query.get(current_user_id)

    if not user:
        return make_response(jsonify({"message": "User not found"}), 404)

    # Delete the user record from the database
    db.session.delete(user)
    db.session.commit()

    return make_response(jsonify({"message": "User deleted successfully"}), 200)

# Add/update/delete routes if required

