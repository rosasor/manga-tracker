from flask import Blueprint, request, render_template
from models.manga import Manga  # Import the Manga model

manga_bp = Blueprint('manga', __name__)

user_lists = {
    'reading': [],
    'plan_to_read': [],
    'dropped': []
}

@manga_bp.route('/search')
def search():
    name = request.args.get('name', '')
    genre = request.args.get('genre', '')
    manga = Manga.query.filter(
        Manga.name.ilike(f'%{name}%'),
        Manga.genre.ilike(f'%{genre}%')
    ).all()
    
    # Render the 'search.html' template and pass manga list as context
    return render_template('search.html', manga_list=manga)