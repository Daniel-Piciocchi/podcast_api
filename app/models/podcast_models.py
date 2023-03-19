from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.genre_models import Genre
from app.models.user_models import User


# Podcast model


class Podcast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, index=True)
    author = db.relationship('User', backref='podcasts')
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genre.id'), nullable=False, index=True)
    genre = db.relationship('Genre', backref='podcasts')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

# Podcast schema


class PodcastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Podcast
        load_instance = True
        include_fk = True