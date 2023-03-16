from flask import Flask
from .user_routes import user_bp
from .podcast_routes import podcast_bp
from .episode_routes import episode_bp
from .rating_routes import rating_bp
from .genre_routes import genre_bp
from .search_routes import search_bp

def init_app(app: Flask):
    app.register_blueprint(user_bp)
    app.register_blueprint(podcast_bp)
    app.register_blueprint(episode_bp)
    app.register_blueprint(rating_bp)
    app.register_blueprint(genre_bp)
    app.register_blueprint(search_bp)
