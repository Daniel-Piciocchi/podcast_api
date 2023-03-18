from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Rating, RatingSchema
from app.utils import admin_required

rating_bp = Blueprint("rating_bp", __name__)
rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)

# Add a new rating


@app.route('/api/ratings', methods=['POST'])
@jwt_required()
def add_rating():
    user_id = get_jwt_identity()
    podcast_id = request.json.get('podcast_id', None)
    rating_value = request.json.get('rating_value', None)

    if not podcast_id or rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Create a new rating and add it to the database
    new_rating = Rating(
        user_id=user_id, podcast_id=podcast_id, rating=rating_value)
    db.session.add(new_rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating added successfully"}), 201)

# Get all ratings


@app.route('/api/ratings', methods=['GET'])
def get_all_ratings():
    # Query the database for all Rating records
    ratings = Rating.query.all()
    result = ratings_schema.dump(ratings)
    return make_response(jsonify(result), 200)

# Get a specific rating


@app.route('/api/ratings/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    # Query the database for a specific Rating record by its ID
    rating = Rating.query.get(rating_id)
    
    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    result = rating_schema.dump(rating)
    return make_response(jsonify(result), 200)

# Update a specific rating
@app.route('/api/ratings/<int:rating_id>', methods=['PUT'])
@jwt_required()
def update_rating(rating_id):
    user_id = get_jwt_identity()
    # Query the database for a specific Rating record by its ID
    rating = Rating.query.get(rating_id)

    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    rating_value = request.json.get('rating_value', None)

    if rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    # Update the rating value and save it to the database
    rating.rating = rating_value
    db.session.commit()

    return make_response(jsonify({"message": "Rating updated successfully"}), 200)



@app.route('/api/ratings/<int:rating_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_rating(rating_id):
    user_id = get_jwt_identity()
    # Query the database for a specific Rating record by its ID
    rating = Rating.query.get(rating_id)

    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    # Delete the Rating record from the database
    db.session.delete(rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating deleted successfully"}), 200)
