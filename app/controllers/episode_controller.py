from flask import request, jsonify, make_response
from app import db
from app.models.episode_models import Episode, EpisodeSchema
from app.utils import admin_required

episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)

@admin_required
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

def get_all_episodes():
    episodes = Episode.query.all()
    result = episodes_schema.dump(episodes)
    return make_response(jsonify(result), 200)

def get_episode(episode_id):
    episode = Episode.query.get(episode_id)

    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    result = episode_schema.dump(episode)
    return make_response(jsonify(result), 200)

@admin_required
def update_episode(episode_id):
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

    db.session.commit()

    return make_response(jsonify({"message": "Episode updated successfully"}), 200)

@admin_required
def delete_episode(episode_id):
    episode = Episode.query.get(episode_id)

    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    db.session.delete(episode)
    db.session.commit()

    return make_response(jsonify({"message": "Episode deleted successfully"}), 200)
