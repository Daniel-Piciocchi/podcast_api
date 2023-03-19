from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# Rating model


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)
    user = db.relationship('User', backref='ratings')
    podcast_id = db.Column(db.Integer, db.ForeignKey(
        'podcast.id'), nullable=False, index=True)
    podcast = db.relationship('Podcast', backref='ratings')
    rating = db.Column(db.Integer, nullable=False)


# Rating schema


class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True
        include_fk = True

