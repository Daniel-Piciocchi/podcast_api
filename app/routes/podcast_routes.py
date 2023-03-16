from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Podcast, User, PodcastSchema

podcast_bp = Blueprint("podcast_bp", __name__)
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)


@app.route('/api/podcasts', methods=['POST'])
@jwt_required()
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


@app.route('/api/podcasts', methods=['GET'])
def get_all_podcasts():
    podcasts = Podcast.query.all()
    result = podcasts_schema.dump(podcasts)
    return make_response(jsonify(result), 200)


@app.route('/api/podcasts/<int:podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)
    result = podcast_schema.dump(podcast)
    return make_response(jsonify(result), 200)


@app.route('/api/podcasts/<int:podcast_id>', methods=['PUT'])
@jwt_required()
def update_podcast(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)

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


@app.route('/api/podcasts/<int:podcast_id>', methods=['DELETE'])
@jwt_required()
def delete_podcast(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)

    db.session.delete(podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast deleted successfully"}), 200)
