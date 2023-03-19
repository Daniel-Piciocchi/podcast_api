from datetime import datetime
from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# User model


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,
                         nullable=False, index=True)  # Username field
    email = db.Column(db.String(120), unique=True,
                      nullable=False, index=True)  # Email field
    password_hash = db.Column(
        db.String(128), nullable=False)  # Password hash field
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag

    # Generates a password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Checks if the provided password matches the stored password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User schema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
