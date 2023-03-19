from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# Episode model


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.String, nullable=True)
    podcast_id = db.Column(db.Integer, db.ForeignKey(
        'podcast.id'), nullable=False, index=True)
    podcast = db.relationship('Podcast', backref='episodes')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

# Episode schema


class EpisodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Episode
        load_instance = True
        include_fk = True