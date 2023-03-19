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
        data = request.get_json(force=True)
    except BadRequest:
        return make_response(jsonify({"message": "Failed to decode JSON object: Please input a valid title, description, author_id, and genre_id"}), 400)

    title = data.get('title', None)
    description = data.get('description', None)
    author_id = data.get('author_id', None)
    genre_id = data.get('genre_id', None)

    if not title or not description or not author_id or not genre_id:
        error_message = {"message": "Missing required data"}
        print(error_message)
        return make_response(jsonify({"message": "Failed to load data: Please input a valid title, description, author_id, and genre_id in JSON format"}), 400)

    # Create a new podcast object and add it to the database
    new_podcast = Podcast(title=title, description=description,
                          author_id=author_id, genre_id=genre_id)
    db.session.add(new_podcast)
    db.session.commit()

    return make_response(jsonify({"message": "Podcast added successfully"}), 201)


def get_all_podcasts():
    try:
        podcasts = Podcast.query.all()
        result = podcasts_schema.dump(podcasts)
        return make_response(jsonify(result), 200)
    except SQLAlchemyError as e:
        return make_response(jsonify({"message": "An error occurred while retrieving podcasts"}), 500)


def get_podcast(podcast_id):
    try:
        podcast = Podcast.query.get(podcast_id)

        if podcast is None:
            return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

        result = podcast_schema.dump(podcast)
        return make_response(jsonify(result), 200)
    except SQLAlchemyError as e:
        return make_response(jsonify({"message": "An error occurred while retrieving the podcast"}), 500)


@admin_required
def update_podcast(user_id, podcast_id):
    try:
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
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while updating the podcast"}), 500)


@admin_required
def delete_podcast(user_id, podcast_id):
    try:
        podcast = Podcast.query.get(podcast_id)

        if podcast is None:
            return make_response(jsonify({"message": "There is no podcast with that ID"}), 404)

        db.session.delete(podcast)
        db.session.commit()

        return make_response(jsonify({"message": "Podcast deleted successfully"}), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while deleting the podcast"}), 500)
    except Exception as e:
        return make_response(jsonify({"message": "An error occurred while deleting the podcast"}), 500)
