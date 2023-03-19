from flask import request, jsonify, make_response
from app import db
from app.models.user_models import User, UserSchema
from app.utils import admin_required
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import  NotFound

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        is_admin = data.get('is_admin', True)

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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login_user():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username or not password:
            return make_response(jsonify({"message": "Missing username or password"}), 400)

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id, additional_claims={
                                               "is_admin": user.is_admin})
            return make_response(jsonify({"access_token": access_token}), 200)
        else:
            return make_response(jsonify({"message": "Invalid username or password"}), 401)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_required
def get_all_users():
    try:
        users = User.query.all()
        result = users_schema.dump(users)
        return make_response(jsonify(result), 200)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_required
def get_user(user_id):
    try:
        user = User.query.get_or_404(
            user_id, description="There is no user with that ID")
        result = user_schema.dump(user)
        return make_response(jsonify(result), 200)
    except Exception as e:
        if (type(e)==NotFound):
            return make_response(jsonify({"message": e.__str__()}), 404)

        return make_response(jsonify({"message": "An error occurred while retrieving user information"}), 500)

def get_user_profile(user_id):
    try:
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
    except Exception as e:
        return make_response(jsonify({"message": "An error occurred while retrieving user profile information"}), 500)

def update_user_profile(user_id):
    try:
        user = User.query.get(user_id)

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
    except Exception as e:
        return make_response(jsonify({"message": "An error occurred while updating user profile information"}), 500)

def delete_user(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({"message": "An error occurred while deleting user information"}), 500)
