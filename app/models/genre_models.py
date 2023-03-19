from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# Genre model


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)

# Genre schema


class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True
        include_fk = True