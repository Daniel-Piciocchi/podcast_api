from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Podcast, User, PodcastSchema

podcast_bp = Blueprint("podcast_bp", __name__)
podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)

# Add a new podcast


@app.route('/api/podcasts', methods=['POST'])
@jwt_required()
def add_podcast():
    title = request.json.get('title', None)
    description = request.json.get('description', None)
    author_id = request.json.get('author_id', None)
    genre_id = request.json.get('genre_id', None)

    if not title or not description or not author_id or not genre_id:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Find the author by the provided author_id
    author = User.query.get(author_id)
    if not author:
        return make_response(jsonify({"message": "Author not found"}), 404)

    # Create a new Podcast instance and add it to the database
    new_podcast = Podcast(title=title, description=description,
                          author_id=author_id, genre_id=genre_id)
    db.session.add(new_podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast added successfully"}), 201)

# Retrieve all podcasts


@app.route('/api/podcasts', methods=['GET'])
def get_all_podcasts():
    # Query the database for all Podcast records
    podcasts = Podcast.query.all()
    result = podcasts_schema.dump(podcasts)
    return make_response(jsonify(result), 200)

# Retrieve a single podcast by its ID


@app.route('/api/podcasts/<int:podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    # Query the database for the Podcast with the given ID, return a 404 if not found
    podcast = Podcast.query.get_or_404(podcast_id)
    result = podcast_schema.dump(podcast)
    return make_response(jsonify(result), 200)

# Update a podcast


@app.route('/api/podcasts/<int:podcast_id>', methods=['PUT'])
@jwt_required()
def update_podcast(podcast_id):
    # Query the database for the Podcast with the given ID, return a 404 if not found
    podcast = Podcast.query.get_or_404(podcast_id)

    title = request.json.get('title', None)
    description = request.json.get('description', None)
    genre_id = request.json.get('genre_id', None)

    if not title or not description or not genre_id:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Update the Podcast attributes with the provided data
    podcast.title = title
    podcast.description = description
    podcast.genre_id = genre_id

    # Commit the changes to the database
    db.session.commit()

    return make_response(jsonify({"message": "Podcast updated successfully"}), 200)

# Delete a podcast


@app.route('/api/podcasts/<int:podcast_id>', methods=['DELETE'])
@jwt_required()
def delete_podcast(podcast_id):
    # Query the database for the Podcast with the given ID, return a 404 if not found
    podcast = Podcast.query.get_or_404(podcast_id)

    # Remove the Podcast from the database
    db.session.delete(podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast deleted successfully"}), 200)
