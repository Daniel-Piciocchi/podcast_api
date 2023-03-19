from flask import Blueprint
from app.controllers.genre_controller import add_genre, get_all_genres, get_genre, update_genre, delete_genre
from app.utils import authenticate
from flask_jwt_extended import jwt_required

genre_bp = Blueprint("genre_bp", __name__)

genre_bp.route('/api/genres', methods=['POST'])(jwt_required()(authenticate(add_genre)))
genre_bp.route('/api/genres', methods=['GET'])(get_all_genres)
genre_bp.route('/api/genres/<int:genre_id>', methods=['GET'])(get_genre)
genre_bp.route('/api/genres/<int:genre_id>', methods=['PUT'])(jwt_required()(authenticate(update_genre)))
genre_bp.route('/api/genres/<int:genre_id>', methods=['DELETE'])(jwt_required()(authenticate(delete_genre)))
