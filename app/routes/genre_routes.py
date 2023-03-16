from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Genre, GenreSchema

genre_bp = Blueprint("genre_bp", __name__)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@app.route('/api/genres', methods=['POST'])
@jwt_required()
def add_genre():
    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    new_genre = Genre(name=name)
    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre added successfully"}), 201)


@app.route('/api/genres', methods=['GET'])
def get_all_genres():
    genres = Genre.query.all()
    result = genres_schema.dump(genres)
    return make_response(jsonify(result), 200)


@app.route('/api/genres/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    result = genre_schema.dump(genre)
    return make_response(jsonify(result), 200)


@app.route('/api/genres/<int:genre_id>', methods=['PUT'])
@jwt_required()
def update_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    genre.name = name
    db.session.commit()

    return make_response(jsonify({"message": "Genre updated successfully"}), 200)


@app.route('/api/genres/<int:genre_id>', methods=['DELETE'])
@jwt_required()
def delete_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)

    db.session.delete(genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre deleted successfully"}), 200)
