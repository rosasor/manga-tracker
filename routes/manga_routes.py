from flask import Blueprint, request, jsonify
from models.user_manga_list import UserMangaList
from models.manga import Manga
from app import db
from .auth_routes import jwt_required

manga_bp = Blueprint('manga', __name__)

# Fetch manga with filters and pagination
@manga_bp.route('/api/manga', methods=['GET'])
def get_manga():
    name, genre = request.args.get('name', ''), request.args.get('genre', '')
    manga_type, status = request.args.getlist('type'), request.args.getlist('status')
    page, per_page = request.args.get('page', 1, type=int), request.args.get('per_page', 30, type=int)

    query = Manga.query
    if name: query = query.filter(Manga.name.ilike(f'%{name}%'))
    if genre: query = query.filter(Manga.genre.ilike(f'%{genre}%'))
    if manga_type: query = query.filter(Manga.type.in_(manga_type))
    if status: query = query.filter(Manga.status.in_(status))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'manga': [manga.to_dict() for manga in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    })

# Add or update manga in user's list
@manga_bp.route('/api/manga_list', methods=['POST'])
@jwt_required
def add_to_list():
    data = request.json
    user_id = request.user["id"]
    manga_id, list_type = data.get("manga_id"), data.get("list_type")

    if not manga_id or not list_type:
        return jsonify({"message": "Manga ID and list type are required"}), 400

    existing_entry = UserMangaList.query.filter_by(user_id=user_id, manga_id=manga_id).first()
    if existing_entry:
        existing_entry.list_type = list_type
    else:
        db.session.add(UserMangaList(user_id=user_id, manga_id=manga_id, list_type=list_type))

    db.session.commit()
    return jsonify({"message": f"Manga {manga_id} added to {list_type} list for user {user_id}."}), 200

# Fetch user's manga list
@manga_bp.route('/api/manga_list', methods=['GET'])
@jwt_required
def get_user_manga_list():
    user_id = request.user["id"]
    user_lists = UserMangaList.query.filter_by(user_id=user_id).all()
    result = {}
    for entry in user_lists:
        result.setdefault(entry.list_type, []).append(entry.manga.to_dict())
    return jsonify(result), 200
