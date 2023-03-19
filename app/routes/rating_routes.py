from flask import Blueprint
from app.controllers.rating_controller import add_rating, get_all_ratings, get_rating, update_rating, delete_rating
from app.utils import authenticate
from flask_jwt_extended import jwt_required

rating_bp = Blueprint("rating_bp", __name__)

rating_bp.route('/api/ratings', methods=['POST'])(jwt_required()(authenticate(add_rating)))
rating_bp.route('/api/ratings', methods=['GET'])(get_all_ratings)
rating_bp.route('/api/ratings/<int:rating_id>', methods=['GET'])(get_rating)
rating_bp.route('/api/ratings/<int:rating_id>', methods=['PUT'])(jwt_required()(authenticate(update_rating)))
rating_bp.route('/api/ratings/<int:rating_id>', methods=['DELETE'])(jwt_required()(authenticate(delete_rating)))
