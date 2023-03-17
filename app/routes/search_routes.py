from flask import Blueprint, request
from sqlalchemy import or_, func
from app.models import Podcast, Episode
from app import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')

    podcasts = Podcast.query.filter(
        or_(
            func.lower(Podcast.title).like(func.lower(f'%{keyword}%')),
            func.lower(Podcast.author).like(func.lower(f'%{keyword}%'))
        )
    ).all()

    episodes = Episode.query.filter(
        or_(
            func.lower(Episode.title).like(func.lower(f'%{keyword}%')),
            func.lower(Episode.description).like(func.lower(f'%{keyword}%'))
        )
    ).all()

    podcast_results = [podcast.to_dict() for podcast in podcasts]
    episode_results = [episode.to_dict() for episode in episodes]

    return {
        'podcasts': podcast_results,
        'episodes': episode_results
    }
