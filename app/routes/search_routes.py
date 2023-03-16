from flask import Blueprint, request
from sqlalchemy import or_
from app.models import Podcast, Episode
from app import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')

    podcasts = Podcast.query.filter(
        or_(
            Podcast.title.ilike(f'%{keyword}%'),
            Podcast.author.ilike(f'%{keyword}%')
        )
    ).all()

    episodes = Episode.query.filter(
        or_(
            Episode.title.ilike(f'%{keyword}%'),
            Episode.description.ilike(f'%{keyword}%')
        )
    ).all()

    podcast_results = [podcast.to_dict() for podcast in podcasts]
    episode_results = [episode.to_dict() for episode in episodes]

    return {
        'podcasts': podcast_results,
        'episodes': episode_results
    }
