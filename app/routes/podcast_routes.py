from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from app import app, db
from app.models import Podcast, User, PodcastSchema
from app.utils import admin_required

podcast_bp = Blueprint("podcast_bp", __name__)
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)

# Adds a new podcast


@podcast_bp.route('/api/podcasts', methods=['POST'])
@jwt_required()
@admin_required
def add_podcast():
    title = request.json.get('title', None)
    description = request.json.get('description', None)
    author_id = request.json.get('author_id', None)
    genre_id = request.json.get('genre_id', None)

    if not title or not description or not author_id or not genre_id:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Finds the author by the provided author_id
    author = User.query.get(author_id)
    if not author:
        return make_response(jsonify({"message": "Author not found"}), 404)

    # Creates a new Podcast instance and adds it to the database
    new_podcast = Podcast(title=title, description=description,
                          author_id=author_id, genre_id=genre_id)
    db.session.add(new_podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast added successfully"}), 201)

# Retrieves all podcasts


@podcast_bp.route('/api/podcasts', methods=['GET'])
def get_all_podcasts():
    # Queries the database for all Podcast records
    podcasts = Podcast.query.all()
    result = podcasts_schema.dump(podcasts)
    return make_response(jsonify(result), 200)

# Retrieves a single podcast by its ID


@podcast_bp.route('/api/podcasts/<int:podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    # Queries the database for the Podcast with the given ID
    podcast = Podcast.query.get(podcast_id)

    if podcast is None:
        return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

    result = podcast_schema.dump(podcast)
    return make_response(jsonify(result), 200)

# Updates a podcast


@podcast_bp.route('/api/podcasts/<int:podcast_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_podcast(podcast_id):
    # Queries the database for the Podcast with the given ID
    podcast = Podcast.query.get(podcast_id)

    if podcast is None:
        return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

    title = request.json.get('title', None)
    description = request.json.get('description', None)
    genre_id = request.json.get('genre_id', None)

    if not title or not description or not genre_id:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Updates the Podcast attributes with the provided data
    podcast.title = title
    podcast.description = description
    podcast.genre_id = genre_id

    # Commits the changes to the database
    db.session.commit()

    return make_response(jsonify({"message": "Podcast updated successfully"}), 200)

# Deletes a podcast


@podcast_bp.route('/api/podcasts/<int:podcast_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_podcast(podcast_id):
    # Queries the database for the Podcast with the given ID
    podcast = Podcast.query.get(podcast_id)

    if podcast is None:
        return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

    # Removes the Podcast from the database
    db.session.delete(podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast deleted successfully"}), 200)
