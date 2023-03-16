from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Episode, User, EpisodeSchema

episode_bp = Blueprint("episode_bp", __name__)
episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)


@app.route('/api/episodes', methods=['POST'])
@jwt_required()
def add_episode():
    title = request.json.get('title', None)
    podcast_id = request.json.get('podcast_id', None)
    description = request.json.get('description', None)

    if not title or not podcast_id or not description:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    new_episode = Episode(
        title=title, podcast_id=podcast_id, description=description)
    db.session.add(new_episode)
    db.session.commit()

    return make_response(jsonify({"message": "Episode added successfully"}), 201)


@app.route('/api/episodes', methods=['GET'])
def get_all_episodes():
    episodes = Episode.query.all()
    result = episodes_schema.dump(episodes)
    return make_response(jsonify(result), 200)


@app.route('/api/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    result = episode_schema.dump(episode)
    return make_response(jsonify(result), 200)


@app.route('/api/episodes/<int:episode_id>', methods=['PUT'])
@jwt_required()
def update_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)

    title = request.json.get('title', None)
    podcast_id = request.json.get('podcast_id', None)
    description = request.json.get('description', None)

    if title:
        episode.title = title
    if podcast_id:
        episode.podcast_id = podcast_id
    if description:
        episode.description = description

    db.session.commit()

    return make_response(jsonify({"message": "Episode updated successfully"}), 200)


@app.route('/api/episodes/<int:episode_id>', methods=['DELETE'])
@jwt_required()
def delete_episode(episode_id):
    episode = Episode.query.get_or_404(episode_id)
    db.session.delete(episode)
    db.session.commit()

    return make_response(jsonify({"message": "Episode deleted successfully"}), 200)
