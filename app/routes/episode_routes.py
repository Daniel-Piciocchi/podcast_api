from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Episode, User, EpisodeSchema
from app.utils import admin_required

episode_bp = Blueprint("episode_bp", __name__)
episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)

# Add a new episode
@episode_bp.route('/api/episodes', methods=['POST'])
@jwt_required()
@admin_required
def add_episode():
    title = request.json.get('title', None)
    podcast_id = request.json.get('podcast_id', None)
    description = request.json.get('description', None)

    if not title or not podcast_id or not description:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Create a new Episode instance and add it to the database
    new_episode = Episode(
        title=title, podcast_id=podcast_id, description=description)
    db.session.add(new_episode)
    db.session.commit()

    return make_response(jsonify({"message": "Episode added successfully"}), 201)

# Retrieve all episodes
@episode_bp.route('/api/episodes', methods=['GET'])
def get_all_episodes():
    # Query the database for all Episode records
    episodes = Episode.query.all()
    result = episodes_schema.dump(episodes)
    return make_response(jsonify(result), 200)

# Retrieve a single episode by its ID
@episode_bp.route('/api/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    # Query the database for the Episode with the given ID, return a 404 if not found
    episode = Episode.query.get(episode_id)

    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)
        
    result = episode_schema.dump(episode)
    return make_response(jsonify(result), 200)

# Update an episode
@episode_bp.route('/api/episodes/<int:episode_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_episode(episode_id):
    # Query the database for the Episode with the given ID
    episode = Episode.query.get(episode_id)

    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    title = request.json.get('title', None)
    podcast_id = request.json.get('podcast_id', None)
    description = request.json.get('description', None)

    if title:
        episode.title = title
    if podcast_id:
        episode.podcast_id = podcast_id
    if description:
        episode.description = description

    # Commit the changes to the database
    db.session.commit()

    return make_response(jsonify({"message": "Episode updated successfully"}), 200)

# Delete an episode
@episode_bp.route('/api/episodes/<int:episode_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_episode(episode_id):
    # Query the database for the Episode with the given ID
    episode = Episode.query.get(episode_id)

    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    # Remove the Episode from the database
    db.session.delete(episode)
    db.session.commit()

    return make_response(jsonify({"message": "Episode deleted successfully"}), 200)

