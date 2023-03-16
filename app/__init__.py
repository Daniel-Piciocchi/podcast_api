import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podcast_api.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
# CORS(app)

# Import the routes after the app has been created to avoid circular import issues.
from app.routes import user_routes, podcast_routes, episode_routes, rating_routes, genre_routes

app.register_blueprint(user_routes.user_bp)
app.register_blueprint(podcast_routes.podcast_bp)
app.register_blueprint(episode_routes.episode_bp)
app.register_blueprint(rating_routes.rating_bp)
app.register_blueprint(genre_routes.genre_bp)