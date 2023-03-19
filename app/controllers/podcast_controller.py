from flask import request, jsonify, make_response
from app import db
from app.models.podcast_models import Podcast, User, PodcastSchema
from app.utils import admin_required

podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)

@admin_required
def add_podcast():
    title = request.json.get('title', None)
    description = request.json.get('description', None)
    author_id = request.json.get('author_id', None)
    genre_id = request.json.get('genre_id', None)

    if not title or not description or not author_id or not genre_id:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    author = User.query.get(author_id)
    if not author:
        return make_response(jsonify({"message": "Author not found"}), 404)

    new_podcast = Podcast(title=title, description=description, author_id=author_id, genre_id=genre_id)
    db.session.add(new_podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast added successfully"}), 201)

def get_all_podcasts():
    podcasts = Podcast.query.all()
    result = podcasts_schema.dump(podcasts)
    return make_response(jsonify(result), 200)

def get_podcast(podcast_id):
    podcast = Podcast.query.get(podcast_id)

    if podcast is None:
        return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

    result = podcast_schema.dump(podcast)
    return make_response(jsonify(result), 200)

@admin_required
def update_podcast(podcast_id):
    podcast = Podcast.query.get(podcast_id)

    if podcast is None:
        return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

    title = request.json.get('title', None)
    description = request.json.get('description', None)
    genre_id = request.json.get('genre_id', None)

    if not title or not description or not genre_id:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    podcast.title = title
    podcast.description = description
    podcast.genre_id = genre_id

    db.session.commit()

    return make_response(jsonify({"message": "Podcast updated successfully"}), 200)

@admin_required
def delete_podcast(podcast_id):
    podcast = Podcast.query.get(podcast_id)

    if podcast is None:
        return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

    db.session.delete(podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast deleted successfully"}), 200)
