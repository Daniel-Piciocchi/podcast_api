from flask import Blueprint
from app.controllers.podcast_controller import add_podcast, get_all_podcasts, get_podcast, update_podcast, delete_podcast
from app.utils import authenticate
from flask_jwt_extended import jwt_required

podcast_bp = Blueprint("podcast_bp", __name__)

podcast_bp.route('/api/podcasts', methods=['POST'])(jwt_required()(authenticate(add_podcast)))
podcast_bp.route('/api/podcasts', methods=['GET'])(get_all_podcasts)
podcast_bp.route('/api/podcasts/<int:podcast_id>', methods=['GET'])(get_podcast)
podcast_bp.route('/api/podcasts/<int:podcast_id>', methods=['PUT'])(jwt_required()(authenticate(update_podcast)))
podcast_bp.route('/api/podcasts/<int:podcast_id>', methods=['DELETE'])(jwt_required()(authenticate(delete_podcast)))
