from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# Episode model
class Episode(db.Model):
    # defining the Episode model
    id = db.Column(db.Integer, primary_key=True) # defining a primary key column for the episode id
    title = db.Column(db.String(120), nullable=False, index=True) # defining a title column for the episode with max 120 chars
    description = db.Column(db.String, nullable=True) # defining a description column for the episode
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcast.id'), nullable=False, index=True) # defining a foreign key to link episodes to podcasts
    podcast = db.relationship('Podcast', backref='episodes') # defining a relationship with Podcast model to access episodes of a podcast
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True) # defining a column to store the date and time of episode creation

# Episode schema
class EpisodeSchema(ma.SQLAlchemyAutoSchema):
    # defining the schema for Episode
    class Meta:
        model = Episode # linking the schema to Episode model
        load_instance = True # allows deserialization of objects to instance of model class
        include_fk = True # includes foreign keys in serialized output
