from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# Genre model
class Genre(db.Model):
    # The Genre class represents the database table for genres, with columns for id and name.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

# Genre schema
class GenreSchema(ma.SQLAlchemyAutoSchema):
    # The GenreSchema class specifies how to serialize and deserialize Genre objects
    class Meta:
        model = Genre  # the model that this schema corresponds to is the Genre model
        load_instance = True  # enables deserialization to generate and return a Genre instance
        include_fk = True  # includes foreign keys in serialized output (e.g. podcast_id)
