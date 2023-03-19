from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from app.models import Rating, RatingSchema
from app.utils import admin_required

rating_bp = Blueprint("rating_bp", __name__)
rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)

# Adds a new rating


@app.route('/api/ratings', methods=['POST'])
@jwt_required()
def add_rating():
    user_id = get_jwt_identity()
    podcast_id = request.json.get('podcast_id', None)
    rating_value = request.json.get('rating_value', None)

    if not podcast_id or rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Creates a new rating and adds it to the database
    new_rating = Rating(
        user_id=user_id, podcast_id=podcast_id, rating=rating_value)
    db.session.add(new_rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating added successfully"}), 201)

# Gets all ratings


@app.route('/api/ratings', methods=['GET'])
def get_all_ratings():
    # Queries the database for all Rating records
    ratings = Rating.query.all()
    result = ratings_schema.dump(ratings)
    return make_response(jsonify(result), 200)

# Gets a specific rating


@app.route('/api/ratings/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    # Queries the database for a specific Rating record by its ID
    rating = Rating.query.get(rating_id)
    
    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    result = rating_schema.dump(rating)
    return make_response(jsonify(result), 200)

# Updates a specific rating
@app.route('/api/ratings/<int:rating_id>', methods=['PUT'])
@jwt_required()
def update_rating(rating_id):
    user_id = get_jwt_identity()
    # Queries the database for a specific Rating record by its ID
    rating = Rating.query.get(rating_id)

    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    rating_value = request.json.get('rating_value', None)

    if rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Updates the rating value and saves it to the database
    rating.rating = rating_value
    db.session.commit()

    return make_response(jsonify({"message": "Rating updated successfully"}), 200)



@app.route('/api/ratings/<int:rating_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_rating(rating_id):
    user_id = get_jwt_identity()
    # Queries the database for a specific Rating record by its ID
    rating = Rating.query.get(rating_id)

    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    # Deletes the Rating record from the database
    db.session.delete(rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating deleted successfully"}), 200)
