from flask import request, jsonify, make_response
from app import db
from app.models.genre_models import Genre, GenreSchema
from app.utils import admin_required
from sqlalchemy.exc import SQLAlchemyError

# Initializes the genre schema
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@admin_required
def add_genre(user_id):
    try:
        # Gets the genre name from the request
        name = request.json.get('name', None)

        # Checks if the name is provided
        if not name:
            return make_response(jsonify({"message": "Missing required data"}), 400)

        # Creates a new genre instance and add it to the database
        new_genre = Genre(name=name)
        db.session.add(new_genre)
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Genre added successfully"}), 201)
    except SQLAlchemyError as e:
        # Rollsback the transaction and returns an error message if an error occurs
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while adding the genre"}), 500)
    except Exception as e:
        # Returns an error message if any other exception occurs
        return make_response(jsonify({"message": "An error occurred while adding the genre"}), 500)


def get_all_genres():
    try:
        # Queries all genres from the database
        genres = Genre.query.all()
        # Serializes the genres using the genres schema
        result = genres_schema.dump(genres)
        # Returns the serialized genres as a JSON response
        return make_response(jsonify(result), 200)
    except Exception as e:
        # Returns an error message if any exception occurs
        return make_response(jsonify({"message": "An error occurred while getting all genres"}), 500)


def get_genre(user_id, genre_id):
    try:
        # Queries the genre by ID from the database
        genre = Genre.query.get(genre_id)

        # Checks if the genre exists
        if genre is None:
            return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

        # Serializes the genre using the genre schema
        result = genre_schema.dump(genre)
        # Returns the serialized genre as a JSON response
        return make_response(jsonify(result), 200)
    except Exception as e:
        # Returns an error message if any exception occurs
        return make_response(jsonify({"message": "An error occurred while getting the genre"}), 500)


@admin_required
def update_genre(user_id, genre_id):
    try:
        # Queries the genre by ID from the database
        genre = Genre.query.get(genre_id)

        # Checks if the genre exists
        if genre is None:
            return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

        # Get the new name from the request
        name = request.json.get('name', None)

        # Checks if the name is provided
        if not name:
            return make_response(jsonify({"message": "Missing required data"}), 400)

        # Updates the genre name
        genre.name = name
        # Commits the changes to the database
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Genre updated successfully"}), 200)
    except SQLAlchemyError as e:
        # Rollsback the transaction and returns an error message if an error occurs
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while updating the genre"}), 500)
    except Exception as e:
        # Return an error message if any other exception occurs
        return make_response(jsonify({"message": "An error occurred while updating the genre"}), 500)


@admin_required
def delete_genre(user_id, genre_id):
    try:
        # Queries the genre by ID from the database
        genre = Genre.query.get(genre_id)

        # Checks if the genre exists
        if genre is None:
            return make_response(jsonify({"message": "There is no genre with that ID"}), 404)

        # Checks if the genre has associated podcasts
        if genre.podcasts:
            return make_response(jsonify({"message": "Cannot delete genre with associated podcasts"}), 400)

        # Deletes the genre from the database
        db.session.delete(genre)
        # Commits the changes to the database
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Genre deleted successfully"}), 200)
    except SQLAlchemyError as e:
        # Rollsback the transaction and returns an error message if an error occurs
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while deleting the genre"}), 500)
    except Exception as e:
        # Returns an error message if any other exception occurs
        return make_response(jsonify({"message": "An error occurred while deleting the genre"}), 500)
