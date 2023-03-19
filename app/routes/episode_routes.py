from flask import Blueprint
from app.controllers.episode_controller import add_episode, get_all_episodes, get_episode, update_episode, delete_episode
from app.utils import authenticate
from flask_jwt_extended import jwt_required

episode_bp = Blueprint("episode_bp", __name__)

episode_bp.route('/api/episodes', methods=['POST'])(jwt_required()(authenticate(add_episode)))
episode_bp.route('/api/episodes', methods=['GET'])(get_all_episodes)
episode_bp.route('/api/episodes/<int:episode_id>', methods=['GET'])(get_episode)
episode_bp.route('/api/episodes/<int:episode_id>', methods=['PUT'])(jwt_required()(authenticate(update_episode)))
episode_bp.route('/api/episodes/<int:episode_id>', methods=['DELETE'])(jwt_required()(authenticate(delete_episode)))
