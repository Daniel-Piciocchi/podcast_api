from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from app import app, db
from app.models import Genre, GenreSchema
from app.utils import admin_required

genre_bp = Blueprint("genre_bp", __name__)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

# Adds a new genre


@genre_bp.route('/api/genres', methods=['POST'])
@jwt_required()
@admin_required
def add_genre():
    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Creates a new Genre instance and adds it to the database
    new_genre = Genre(name=name)
    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre added successfully"}), 201)

# Retrieves all genres


@genre_bp.route('/api/genres', methods=['GET'])
def get_all_genres():
    # Queries the database for all Genre records
    genres = Genre.query.all()
    result = genres_schema.dump(genres)
    return make_response(jsonify(result), 200)

# Retrieves a single genre by its ID


@genre_bp.route('/api/genres/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    # Queries the database for the Genre with the given ID
    genre = Genre.query.get(genre_id)

    if genre is None:
        return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

    result = genre_schema.dump(genre)
    return make_response(jsonify(result), 200)

# Updates a genre


@genre_bp.route('/api/genres/<int:genre_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_genre(genre_id):
    # Queries the database for the Genre with the given ID
    genre = Genre.query.get(genre_id)

    if genre is None:
        return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    genre.name = name
    # Commits the changes to the database
    db.session.commit()

    return make_response(jsonify({"message": "Genre updated successfully"}), 200)

# Deletes a genre


@genre_bp.route('/api/genres/<int:genre_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_genre(genre_id):
    # Queries the database for the Genre with the given ID
    genre = Genre.query.get(genre_id)

    if genre is None:
        return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

    # Checks if the Genre has any associated Podcasts
    if genre.podcasts:
        # Returns an error message if there are associated Podcasts
        return make_response(jsonify({"message": "Cannot delete genre with associated podcasts"}), 400)

    # Removes the Genre from the database
    db.session.delete(genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre deleted successfully"}), 200)
