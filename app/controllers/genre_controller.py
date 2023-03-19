from flask import request, jsonify, make_response
from app import db
from app.models.genre_models import Genre, GenreSchema
from app.utils import admin_required

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

@admin_required
def add_genre():
    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    new_genre = Genre(name=name)
    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre added successfully"}), 201)

def get_all_genres():
    genres = Genre.query.all()
    result = genres_schema.dump(genres)
    return make_response(jsonify(result), 200)

def get_genre(genre_id):
    genre = Genre.query.get(genre_id)

    if genre is None:
        return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

    result = genre_schema.dump(genre)
    return make_response(jsonify(result), 200)

@admin_required
def update_genre(genre_id):
    genre = Genre.query.get(genre_id)

    if genre is None:
        return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

    name = request.json.get('name', None)

    if not name:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    genre.name = name
    db.session.commit()

    return make_response(jsonify({"message": "Genre updated successfully"}), 200)

@admin_required
def delete_genre(genre_id):
    genre = Genre.query.get(genre_id)

    if genre is None:
        return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

    if genre.podcasts:
        return make_response(jsonify({"message": "Cannot delete genre with associated podcasts"}), 400)

    db.session.delete(genre)
    db.session.commit()

    return make_response(jsonify({"message": "Genre deleted successfully"}), 200)
