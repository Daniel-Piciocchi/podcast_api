from flask import Blueprint
from app.controllers.search_controller import search

search_bp = Blueprint('search', __name__)

search_bp.route('/api/search', methods=['GET'])(search)
