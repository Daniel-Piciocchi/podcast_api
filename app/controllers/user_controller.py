from flask import request, jsonify, make_response
from app import db
from app.models.user_models import User, UserSchema
from app.utils import admin_required
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import NotFound

user_schema = UserSchema()
users_schema = UserSchema(many=True)


def register_user():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        is_admin = data.get('is_admin', True)

        # Checks if required fields are missing
        if not username or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Checks if the username already exists
        existing_user = User.query.filter(User.username == username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

        # Creates a new user object and adds it to the database
        new_user = User(username=username, email=email, is_admin=is_admin)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        # Returns a success message
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        # If any errors occur, returns an error message
        return jsonify({"error": str(e)}), 500


def login_user():
    try:
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        # Checks if username and password are present in the request
        if not username or not password:
            return make_response(jsonify({"message": "Missing username or password"}), 400)

        # Checks if the user with the given username exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Creates an access token for the user
            access_token = create_access_token(identity=user.id, additional_claims={
                                               "is_admin": user.is_admin})
            # Returns the access token
            return make_response(jsonify({"access_token": access_token}), 200)
        else:
            # If the username or password is invalid, return an error message
            return make_response(jsonify({"message": "Invalid username or password"}), 401)

    except Exception as e:
        # If any errors occur, returns an error message
        return jsonify({"error": str(e)}), 500


@admin_required
def get_all_users():
    try:
        # Queries all users from the database
        users = User.query.all()

        # Serializes the users data into JSON format
        result = users_schema.dump(users)

        # Returns a JSON response with the serialized data
        return make_response(jsonify(result), 200)

    except Exception as e:
        # Returns an error response if an exception occurs
        return jsonify({"error": str(e)}), 500


@admin_required
def get_user(user_id):
    try:
        # Retrieve the user with the specified ID from the database
        user = User.query.get_or_404(
            user_id, description="There is no user with that ID")

        # Serialize the user data into JSON format
        result = user_schema.dump(user)

        # Return a JSON response with the serialized data
        return make_response(jsonify(result), 200)

    except Exception as e:
        # Return an error response if an exception occurs
        if (type(e) == NotFound):
            return make_response(jsonify({"message": e.__str__()}), 404)

        return make_response(jsonify({"message": "An error occurred while retrieving user information"}), 500)


def get_user_profile(user_id):
    try:
        # Retrieve the user with the specified ID from the database
        user = User.query.get(user_id)

        # If no user is found with the specified ID, return a 404 error response
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Serialize the user data into a dictionary
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }

        # Return a JSON response with the serialized user data
        return jsonify({"user": user_data}), 200

    except Exception as e:
        # Return an error response if an exception occurs
        return make_response(jsonify({"message": "An error occurred while retrieving user profile information"}), 500)


def update_user_profile(user_id):
    try:
        # Retrieve the user based on user ID
        user = User.query.get(user_id)

        # If no user found with the provided ID, return 404 error
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        # Get the updated profile information from the request payload
        data = request.get_json()

        # Update the username if provided
        username = data.get('username', None)
        if username:
            user.username = username

        # Update the email if provided
        email = data.get('email', None)
        if email:
            user.email = email

        # Save the changes to the database
        db.session.commit()

        # Return a success message
        return make_response(jsonify({"message": "User profile updated successfully"}), 200)
    except Exception as e:
        # If an error occurred, return a 500 error with an error message
        return make_response(jsonify({"message": "An error occurred while updating user profile information"}), 500)


def delete_user(user_id):
    try:
        # Retrieves the user based on user ID
        user = User.query.get(user_id)

        # If no user found with the provided ID, returns 404 error
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        # Deletes the user from the database
        db.session.delete(user)
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    except Exception as e:
        # If an error occurred, returns a 500 error with an error message
        return make_response(jsonify({"message": "An error occurred while deleting user information"}), 500)
