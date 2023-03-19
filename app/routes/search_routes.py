from flask import Blueprint, request
from sqlalchemy import or_, func
from app.models import Podcast, Episode
from app import db

# Creates a Blueprint for search related routes
search_bp = Blueprint('search', __name__)

# Routes for searching podcasts and episodes by a keyword


@search_bp.route('/api/search', methods=['GET'])
def search():
    # Gets the search keyword from the request query parameters
    keyword = request.args.get('keyword', '')

    # Queries the database for podcasts with titles or authors containing the keyword (case-insensitive)
    podcasts = Podcast.query.filter(
        or_(
            func.lower(Podcast.title).like(func.lower(f'%{keyword}%')),
            func.lower(Podcast.author).like(func.lower(f'%{keyword}%'))
        )
    ).all()

    # Queries the database for episodes with titles or descriptions containing the keyword (case-insensitive)
    episodes = Episode.query.filter(
        or_(
            func.lower(Episode.title).like(func.lower(f'%{keyword}%')),
            func.lower(Episode.description).like(func.lower(f'%{keyword}%'))
        )
    ).all()

    # Converts the podcast results to a list of dictionaries
    podcast_results = [podcast.to_dict() for podcast in podcasts]
    # Converts the episode results to a list of dictionaries
    episode_results = [episode.to_dict() for episode in episodes]

    # Returns the search results as a dictionary containing both podcasts and episodes
    return {
        'podcasts': podcast_results,
        'episodes': episode_results
    }
