from flask import request, jsonify, make_response
from app import db
from app.models.episode_models import Episode, EpisodeSchema
from app.utils import admin_required
from sqlalchemy.exc import SQLAlchemyError

# Initializes episode schemas for serialization
episode_schema = EpisodeSchema()
episodes_schema = EpisodeSchema(many=True)

# Function to add a new episode (requires admin privileges)


@admin_required
def add_episode(user_id):
    # Gets data from the request
    title = request.json.get('title', None)
    podcast_id = request.json.get('podcast_id', None)
    description = request.json.get('description', None)

    # Checks if any required field is missing
    if not title or not podcast_id or not description:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Creates a new episode object
    new_episode = Episode(
        title=title, podcast_id=podcast_id, description=description)

    try:
        # Adds the episode to the database and commit the changes
        db.session.add(new_episode)
        db.session.commit()
    except SQLAlchemyError as e:
        # If an error occurs, rollsback the changes and returns an error message
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while adding the episode"}), 500)
    except Exception as e:
        # Catches any other exceptions and returns an error message
        return make_response(jsonify({"message": "An error occurred while adding the episode"}), 500)

    # Returns a success message
    return make_response(jsonify({"message": "Episode added successfully"}), 201)

# Function to get all episodes


def get_all_episodes():
    try:
        # Queries all episodes from the database
        episodes = Episode.query.all()
    except SQLAlchemyError as e:
        # If an error occurs, returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching episodes"}), 500)
    except Exception as e:
        # Catches any other exceptions and returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching episodes"}), 500)

    # Serializes the episodes and returns them in the response
    result = episodes_schema.dump(episodes)
    return make_response(jsonify(result), 200)

# Function to get a specific episode by ID


def get_episode(episode_id):
    try:
        # Queries the episode by ID
        episode = Episode.query.get(episode_id)
    except SQLAlchemyError as e:
        # If an error occurs, returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching the episode"}), 500)
    except Exception as e:
        # Catches any other exceptions and returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching the episode"}), 500)

    # Checks if the episode exists
    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    # Serializes the episode and returns it in the response
    result = episode_schema.dump(episode)
    return make_response(jsonify(result), 200)

# Function to update an episode (requires admin privileges)


@admin_required
def update_episode(user_id, episode_id):
    try:
        # Fetches the episode by ID
        episode = Episode.query.get(episode_id)
    except SQLAlchemyError as e:
        # If an error occurs, returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching the episode"}), 500)
    except Exception as e:
        # Catches any other exceptions and returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching the episode"}), 500)

    # Checks if the episode exists
    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    # Gets updated data from the request
    title = request.json.get('title', None)
    podcast_id = request.json.get('podcast_id', None)
    description = request.json.get('description', None)

    # Updates the episode fields if they are provided
    if title:
        episode.title = title
    if podcast_id:
        episode.podcast_id = podcast_id
    if description:
        episode.description = description

    try:
        # Commits the changes to the database
        db.session.commit()
    except SQLAlchemyError as e:
        # If an error occurs, rollsback the changes and returns an error message
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while updating the episode"}), 500)
    except Exception as e:
        # Catches any other exceptions and returns an error message
        return make_response(jsonify({"message": "An error occurred while updating the episode"}), 500)

    # Returns a success message
    return make_response(jsonify({"message": "Episode updated successfully"}), 200)

# Function to delete an episode (requires admin privileges)


@admin_required
def delete_episode(user_id, episode_id):
    try:
        # Fetches the episode by ID
        episode = Episode.query.get(episode_id)
    except SQLAlchemyError as e:
        # If an error occurs, returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching the episode"}), 500)
    except Exception as e:
        # Catches any other exceptions and returns an error message
        return make_response(jsonify({"message": "An error occurred while fetching the episode"}), 500)

    # Checks if the episode exists
    if episode is None:
        return make_response(jsonify({"message": "There is no episode with that ID"}), 404)

    try:
        # Deletes the episode from the database and commits the changes
        db.session.delete(episode)
        db.session.commit()
    except SQLAlchemyError as e:
        # If an error occurs, rollsback the changes and returns an error message
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while deleting the episode"}), 500)
    except Exception as e:
        # Catches any other exceptions and returns an error message
        return make_response(jsonify({"message": "An error occurred while deleting the episode"}), 500)

    # Returns a success message
    return make_response(jsonify({"message": "Episode deleted successfully"}), 200)
