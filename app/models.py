from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,
                         nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag

    # Generates a password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks if the provided password matches the stored password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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

# Episode model


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.String, nullable=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey(
        'podcast.id'), nullable=False, index=True)
    podcast = db.relationship('Podcast', backref='episodes')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

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

# Genre model


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

# User schema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True

# Podcast schema


class PodcastSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Podcast
        load_instance = True
        include_fk = True

# Episode schema


class EpisodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Episode
        load_instance = True
        include_fk = True

# Rating schema


class RatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rating
        load_instance = True
        include_fk = True

# Genre schema


class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        include_fk = True
