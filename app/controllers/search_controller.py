from flask import request, jsonify, make_response
from sqlalchemy import or_, func
from app.models.podcast_models import Podcast
from app.models.episode_models import Episode
from app import db

def search():
    try:
        keyword = request.args.get('keyword', '')

        # Searches for podcasts that contain the keyword in their title or author fields
        podcasts = Podcast.query.filter(
            or_(
                func.lower(Podcast.title).like(func.lower(f'%{keyword}%')),
                func.lower(Podcast.author).like(func.lower(f'%{keyword}%'))
            )
        ).all()

        # Searches for episodes that contain the keyword in their title or description fields
        episodes = Episode.query.filter(
            or_(
                func.lower(Episode.title).like(func.lower(f'%{keyword}%')),
                func.lower(Episode.description).like(func.lower(f'%{keyword}%'))
            )
        ).all()

        # Converts results to dictionaries
        podcast_results = [podcast.to_dict() for podcast in podcasts]
        episode_results = [episode.to_dict() for episode in episodes]

        # Returns results as JSON
        return {
            'podcasts': podcast_results,
            'episodes': episode_results
        }

    except Exception as e:
        # Returns error message as JSON with 500 status code
        return make_response(jsonify({"message": "An error occurred while searching"}), 500)
