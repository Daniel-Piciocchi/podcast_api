from flask import request, jsonify, make_response
from app import db
from app.models.rating_models import Rating, RatingSchema
from app.utils import admin_required

rating_schema = RatingSchema()
ratings_schema = RatingSchema(many=True)

def add_rating(user_id):
    podcast_id = request.json.get('podcast_id', None)
    rating_value = request.json.get('rating_value', None)

    if not podcast_id or rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    new_rating = Rating(user_id=user_id, podcast_id=podcast_id, rating=rating_value)
    db.session.add(new_rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating added successfully"}), 201)

def get_all_ratings():
    ratings = Rating.query.all()
    result = ratings_schema.dump(ratings)
    return make_response(jsonify(result), 200)

def get_rating(rating_id):
    rating = Rating.query.get(rating_id)

    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    result = rating_schema.dump(rating)
    return make_response(jsonify(result), 200)

def update_rating(user_id, rating_id):
    rating = Rating.query.get(rating_id)

    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    rating_value = request.json.get('rating_value', None)

    if rating_value is None:
        return make_response(jsonify({"message": "Missing required data"}), 400)

    rating.rating = rating_value
    db.session.commit()

    return make_response(jsonify({"message": "Rating updated successfully"}), 200)

@admin_required
def delete_rating(user_id, rating_id):
    rating = Rating.query.get(rating_id)

    if rating is None:
        return make_response(jsonify({"message": "There is no rating with that ID"}), 404)

    if rating.user_id != user_id:
        return make_response(jsonify({"message": "Unauthorized action"}), 403)

    db.session.delete(rating)
    db.session.commit()

    return make_response(jsonify({"message": "Rating deleted successfully"}), 200)
