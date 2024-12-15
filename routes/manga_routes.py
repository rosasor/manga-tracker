from flask import Blueprint, request, render_template, jsonify
from models.manga import Manga  # Import the Manga model

manga_bp = Blueprint('manga', __name__)

user_lists = {
    'reading': [],
    'plan_to_read': [],
    'dropped': []
}

@manga_bp.route('/api/manga', methods=['GET'])
def get_manga():
    name = request.args.get('name', '')
    genre = request.args.get('genre', '')
    manga = Manga.query.filter(
        Manga.name.ilike(f'%{name}%'),
        Manga.genre.ilike(f'%{genre}%')
    ).all()
    
    # Convert query results to a list of dictionaries and return as JSON
    return jsonify([manga.to_dict() for manga in manga])