from flask import request, jsonify, make_response
from app import db
from app.models.rating_models import Rating, RatingSchema
from app.utils import admin_required
from sqlalchemy.exc import SQLAlchemyError

rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)

def add_rating(user_id):
    try:
        # Gets podcast_id and rating_value from the request JSON
        podcast_id = request.json.get('podcast_id', None)
        rating_value = request.json.get('rating_value', None)

        # Checks if all required attributes are provided
        if not podcast_id or rating_value is None:
            return make_response(jsonify({"message": "Missing required data"}), 400)

        # Creates a new Rating object and adds it to the database
        new_rating = Rating(user_id=user_id, podcast_id=podcast_id, rating=rating_value)
        db.session.add(new_rating)
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Rating added successfully"}), 201)
    except SQLAlchemyError as e:
        # Rollsback the transaction if there is a database error
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while adding the rating"}), 500)

def get_all_ratings():
    try:
        # Queries all ratings from the database
        ratings = Rating.query.all()
        result = ratings_schema.dump(ratings)
        # Returns the list of ratings as a JSON response
        return make_response(jsonify(result), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while retrieving ratings"}), 500)

def get_rating(user_id, rating_id):
    try:
        # Queries the rating by ID from the database
        rating = Rating.query.get(rating_id)

        # Checks if the rating exists
        if rating is None:
            return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

        # Serializes the rating object
        result = rating_schema.dump(rating)
        # Returns the rating as a JSON response
        return make_response(jsonify(result), 200)
    except SQLAlchemyError as e:
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while retrieving the rating"}), 500)


def update_rating(user_id, rating_id):
    try:
        # Queries the rating by ID from the database
        rating = Rating.query.get(rating_id)

        # Checks if the rating exists
        if rating is None:
            return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

        # Checks if the user updating the rating is the same user who created it
        if rating.user_id != user_id:
            return make_response(jsonify({"message": "Unauthorized action"}), 403)

        # Get the new rating_value from the request JSON
        rating_value = request.json.get('rating_value', None)

        # Checks if the new rating value is provided
        if rating_value is None:
            return make_response(jsonify({"message": "Missing required data"}), 400)

        # Updates the rating value and commits the changes
        rating.rating = rating_value
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Rating updated successfully"}), 200)
    except SQLAlchemyError as e:
        # Rollsback the transaction if there is a database error
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while updating the rating"}), 500)

@admin_required
def delete_rating(user_id, rating_id):
    try:
        # Queries the rating by ID from the database
        rating = Rating.query.get(rating_id)

        # Checks if the rating exists
        if rating is None:
            return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

        # Checks if the user deleting the rating is the same user who created it
        if rating.user_id != user_id:
            return make_response(jsonify({"message": "Unauthorized action"}), 403)

        # Deletes the rating from the database and commit the changes
        db.session.delete(rating)
        db.session.commit()

        # Returns a success message
        return make_response(jsonify({"message": "Rating deleted successfully"}), 200)
    except SQLAlchemyError as e:
        # Rollsback the transaction if there is a database error
        db.session.rollback()
        return make_response(jsonify({"message": "An error occurred while deleting the rating"}), 500)
