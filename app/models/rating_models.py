from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# Rating model


class Rating(db.Model):
    # Rating table columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)  # foreign key for user id
    podcast_id = db.Column(db.Integer, db.ForeignKey(
        'podcast.id'), nullable=False, index=True)  # foreign key for podcast id
    rating = db.Column(db.Integer, nullable=False)  # rating value

    # Relationships with other tables
    # establish one-to-many relationship with User table
    user = db.relationship('User', backref='ratings')
    # establish one-to-many relationship with Podcast table
    podcast = db.relationship('Podcast', backref='ratings')

# Rating schema


class RatingSchema(ma.SQLAlchemyAutoSchema):
    # Use the Rating model to create the schema
    class Meta:
        model = Rating
        # Automatically load instance from request data
        load_instance = True
        # Include foreign keys in the schema
        include_fk = True
