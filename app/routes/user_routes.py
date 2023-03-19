from flask import Blueprint
from app.controllers.user_controller import register_user, login_user, get_all_users, get_user, get_user_profile, update_user_profile, delete_user
from app.utils import authenticate
from flask_jwt_extended import jwt_required

user_bp = Blueprint("user_bp", __name__)

user_bp.route('/api/users/register', methods=['POST'])(register_user)
user_bp.route('/api/users/login', methods=['POST'])(login_user)
user_bp.route('/api/users', methods=['GET'])(jwt_required()(authenticate(get_all_users)))
user_bp.route('/api/users/<int:user_id>', methods=['GET'])(jwt_required()(authenticate(get_user)))
user_bp.route('/api/users/profile/<int:user_id>', methods=['GET'])(jwt_required()(get_user_profile))
user_bp.route('/api/users/profile', methods=['PUT'])(jwt_required()(update_user_profile))
user_bp.route('/api/users/delete', methods=['DELETE'])(jwt_required()(delete_user))
