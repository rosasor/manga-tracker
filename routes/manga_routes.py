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
    manga_type = request.args.getlist('type')  # Get list of types
    status = request.args.getlist('status')  # Get list of statuses
    page = request.args.get('page', 1, type=int)  # Default to page 1
    per_page = request.args.get('per_page', 30, type=int)  # Default to 30 items per page

    query = Manga.query

    if name:
        query = query.filter(Manga.name.ilike(f'%{name}%'))
    if genre:
        query = query.filter(Manga.genre.ilike(f'%{genre}%'))
    if manga_type:
        query = query.filter(Manga.type.in_(manga_type))  # Filter by types
    if status:
        query = query.filter(Manga.status.in_(status))  # Filter by statuses


    # Paginate the query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)  # False means don't include total count in the response
    manga_list = pagination.items

    return jsonify({
        'manga': [manga.to_dict() for manga in manga_list],
        'total': pagination.total,  # Return total number of results for pagination controls
        'pages': pagination.pages,  # Return total number of pages
        'current_page': pagination.page  # Return the current page number
    })