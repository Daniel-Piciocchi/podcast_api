from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Genre, GenreSchema

genre_bp = Blueprint("genre_bp", __name__)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

# Add a new genre


@app.route('/api/genres', methods=['POST'])
@jwt_required()
def add_genre():
    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Create a new Genre instance and add it to the database
    new_genre = Genre(name=name)
    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre added successfully"}), 201)

# Retrieve all genres


@app.route('/api/genres', methods=['GET'])
def get_all_genres():
    # Query the database for all Genre records
    genres = Genre.query.all()
    result = genres_schema.dump(genres)
    return make_response(jsonify(result), 200)

# Retrieve a single genre by its ID


@app.route('/api/genres/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    # Query the database for the Genre with the given ID, return a 404 if not found
    genre = Genre.query.get_or_404(genre_id)
    result = genre_schema.dump(genre)
    return make_response(jsonify(result), 200)

# Update a genre


@app.route('/api/genres/<int:genre_id>', methods=['PUT'])
@jwt_required()
def update_genre(genre_id):
    # Query the database for the Genre with the given ID, return a 404 if not found
    genre = Genre.query.get_or_404(genre_id)
    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    genre.name = name
    # Commit the changes to the database
    db.session.commit()

    return make_response(jsonify({"message": "Genre updated successfully"}), 200)

# Delete a genre


@app.route('/api/genres/<int:genre_id>', methods=['DELETE'])
@jwt_required()
def delete_genre(genre_id):
    # Query the database for the Genre with the given ID, return a 404 if not found
    genre = Genre.query.get_or_404(genre_id)

    # Remove the Genre from the database
    db.session.delete(genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre deleted successfully"}), 200)
