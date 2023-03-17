from flask import Blueprint, request
from sqlalchemy import or_
from app.models import Podcast, Episode
from app import db

# Create a blueprint for search
search_bp = Blueprint('search', __name__)

# Route to handle search


@search_bp.route('/search', methods=['GET'])
def search():
    # Get the keyword from the request arguments
    keyword = request.args.get('keyword', '')

    # Query the Podcast model to find podcasts matching the keyword
    # in their title or author fields
    podcasts = Podcast.query.filter(
        or_(
            Podcast.title.ilike(f'%{keyword}%'),
            Podcast.author.ilike(f'%{keyword}%')
        )
    ).all()

    # Query the Episode model to find episodes matching the keyword
    # in their title or description fields
    episodes = Episode.query.filter(
        or_(
            Episode.title.ilike(f'%{keyword}%'),
            Episode.description.ilike(f'%{keyword}%')
        )
    ).all()

    # Convert the podcast results into a list of dictionaries
    podcast_results = [podcast.to_dict() for podcast in podcasts]
    # Convert the episode results into a list of dictionaries
    episode_results = [episode.to_dict() for episode in episodes]

    # Return a dictionary with the search results
    return {
        'podcasts': podcast_results,
        'episodes': episode_results
    }
