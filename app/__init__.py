import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcast_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Added this line

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Import the routes after the app has been created to avoid circular import issues.
from app.routes.search_routes import search_bp
from app.routes import user_routes, podcast_routes, episode_routes, rating_routes, genre_routes

app.register_blueprint(search_bp)
app.register_blueprint(user_routes.user_bp)
app.register_blueprint(podcast_routes.podcast_bp)
app.register_blueprint(episode_routes.episode_bp)
app.register_blueprint(rating_routes.rating_bp)
app.register_blueprint(genre_routes.genre_bp)
