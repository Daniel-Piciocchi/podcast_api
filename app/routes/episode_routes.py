from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from app import app, db
from app.models import Episode, EpisodeSchema
from app.utils import admin_required

episode_bp = Blueprint("episode_bp", __name__)
episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)

# Adds a new episode


@episode_bp.route('/api/episodes', methods=['POST'])
@jwt_required()
@admin_required
def add_episode():
    title = request.json.get('title', None)
    podcast_id = request.json.get('podcast_id', None)
    description = request.json.get('description', None)

    if not title or not podcast_id or not description:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Creates a new Episode instance and adds it to the database
    new_episode = Episode(
        title=title, podcast_id=podcast_id, description=description)
    db.session.add(new_episode)
    db.session.commit()

    return make_response(jsonify({"message": "Episode added successfully"}), 201)

# Retrieves all episodes


@episode_bp.route('/api/episodes', methods=['GET'])
def get_all_episodes():
    # Query the database for all Episode records
    episodes = Episode.query.all()
    result = episodes_schema.dump(episodes)
    return make_response(jsonify(result), 200)

# Retrieves a single episode by its ID


@episode_bp.route('/api/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    # Queries the database for the Episode with the given ID, returns a 404 if not found
    episode = Episode.query.get(episode_id)

    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    result = episode_schema.dump(episode)
    return make_response(jsonify(result), 200)

# Updates an episode


@episode_bp.route('/api/episodes/<int:episode_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_episode(episode_id):
    # Queries the database for the Episode with the given ID
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

    # Commits the changes to the database
    db.session.commit()

    return make_response(jsonify({"message": "Episode updated successfully"}), 200)

# Deletes an episode


@episode_bp.route('/api/episodes/<int:episode_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_episode(episode_id):
    # Queries the database for the Episode with the given ID
    episode = Episode.query.get(episode_id)

    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    # Removes the Episode from the database
    db.session.delete(episode)
    db.session.commit()

    return make_response(jsonify({"message": "Episode deleted successfully"}), 200)
