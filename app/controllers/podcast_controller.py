from flask import request, jsonify, make_response
from app import db
from app.models.podcast_models import Podcast, User, PodcastSchema
from app.utils import admin_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest


podcast_schema = PodcastSchema()
podcasts_schema = PodcastSchema(many=True)


@admin_required
def add_podcast(user_id):
    try:
        # Attempts to get JSON data from the request
        data = request.get_json(force=True)
    except BadRequest:
        # Returns an error message if JSON data is invalid
        return make_response(jsonify({"message": "Failed to decode JSON object: Please input a valid title, description, author_id, and genre_id"}), 400)

    # Extracts podcast attributes from the JSON data
    title = data.get('title', None)
    description = data.get('description', None)
    author_id = data.get('author_id', None)
    genre_id = data.get('genre_id', None)

    # Checks if all required attributes are provided
    if not title or not description or not author_id or not genre_id:
        error_message = {"message": "Missing required data"}
        print(error_message)
        return make_response(jsonify({"message": "Failed to load data: Please input a valid title, description, author_id, and genre_id in JSON format"}), 400)

    # Creates a new podcast object and adds it to the database
    new_podcast = Podcast(title=title, description=description,
                          author_id=author_id, genre_id=genre_id)
    db.session.add(new_podcast)
    db.session.commit()

    # Returns a success message
    return make_response(jsonify({"message": "Podcast added successfully"}), 201)


def get_all_podcasts():
    try:
        # Queries all podcasts from the database
        podcasts = Podcast.query.all()
        # Serializes the podcast objects
        result = podcasts_schema.dump(podcasts)
        # Returns the serialized podcasts
        return make_response(jsonify(result), 200)
    except SQLAlchemyError as e:
        # Returns an error message if there is an issue retrieving podcasts
        return make_response(jsonify({"message": "An error occurred while retrieving podcasts"}), 500)


def get_podcast(podcast_id):
    try:
        # Queries a podcast by ID from the database
        podcast = Podcast.query.get(podcast_id)

        # Checks if the podcast exists
        if podcast is None:
            return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

        # Serializes the podcast object
        result = podcast_schema.dump(podcast)
        # Returns the serialized podcast
        return make_response(jsonify(result), 200)
    except SQLAlchemyError as e:
        # Returns an error message if there is an issue retrieving the podcast
        return make_response(jsonify({"message": "An error occurred while retrieving the podcast"}), 500)


@admin_required
def update_podcast(user_id, podcast_id):
    try:
        # Queries the podcast by ID from the database
        podcast = Podcast.query.get(podcast_id)

        # Checks if the podcast exists
        if podcast is None:
            return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

        # Gets the updated attributes from the request JSON
        title = request.json.get('title', None)
        description = request.json.get('description', None)
        genre_id = request.json.get('genre_id', None)

        # Checks if all required attributes are provided
        if not title or not description or not genre_id:
            return make_response(jsonify({"message": "Missing required data"}), 400)

        # Updates the podcast attributes
        podcast.title = title
        podcast.description = description
        podcast.genre_id = genre_id

        # Commits the changes to the database
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Podcast updated successfully"}), 200)
    except SQLAlchemyError as e:
        # Rollsback the transaction if there is a database error
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while updating the podcast"}), 500)


@admin_required
def delete_podcast(user_id, podcast_id):
    try:
        # Queries the podcast by ID from the database
        podcast = Podcast.query.get(podcast_id)

        # Checks if the podcast exists
        if podcast is None:
            return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

        # Deletes the podcast from the database
        db.session.delete(podcast)
        # Commits the changes to the database
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Podcast deleted successfully"}), 200)
    except SQLAlchemyError as e:
        # Rollsback the transaction if there is a database error
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while deleting the podcast"}), 500)
    except Exception as e:
        return make_response(jsonify({"message": "An error occurred while deleting the podcast"}), 500)
