from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.genre_models import Genre
from app.models.user_models import User


# Podcast model

class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False,
                      index=True)  # The title of the podcast
    # The description of the podcast
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)  # The id of the author of the podcast
    # The relationship with the User model
    author = db.relationship('User', backref='podcasts')
    # The id of the genre the podcast belongs to
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genre.id'), nullable=False, index=True)
    # The relationship with the Genre model
    genre = db.relationship('Genre', backref='podcasts')
    # The timestamp of when the podcast was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

# Podcast schema


class PodcastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Podcast  # The model that the schema is based on
        load_instance = True  # Whether to create instances of the model when deserializing data
        include_fk = True  # Whether to include foreign keys when serializing the model data
