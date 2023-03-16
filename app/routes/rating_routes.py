from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import app, db
from app.models import Rating, RatingSchema

rating_bp = Blueprint("rating_bp", __name__)
rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)


@app.route('/api/ratings', methods=['POST'])
@jwt_required()
def add_rating():
    user_id = get_jwt_identity()
    podcast_id = request.json.get('podcast_id', None)
    rating_value = request.json.get('rating_value', None)

    if not podcast_id or rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    new_rating = Rating(user_id=user_id, podcast_id=podcast_id, rating=rating_value)
    db.session.add(new_rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating added successfully"}), 201)


@app.route('/api/ratings', methods=['GET'])
def get_all_ratings():
    ratings = Rating.query.all()
    result = ratings_schema.dump(ratings)
    return make_response(jsonify(result), 200)


@app.route('/api/ratings/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    rating = Rating.query.get_or_404(rating_id)
    result = rating_schema.dump(rating)
    return make_response(jsonify(result), 200)


@app.route('/api/ratings/<int:rating_id>', methods=['PUT'])
@jwt_required()
def update_rating(rating_id):
    user_id = get_jwt_identity()
    rating = Rating.query.get_or_404(rating_id)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    rating_value = request.json.get('rating_value', None)

    if rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    rating.rating = rating_value
    db.session.commit()

    return make_response(jsonify({"message": "Rating updated successfully"}), 200)


@app.route('/api/ratings/<int:rating_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(rating_id):
    user_id = get_jwt_identity()
    rating = Rating.query.get_or_404(rating_id)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    db.session.delete(rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating deleted successfully"}), 200)
