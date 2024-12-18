from app import db

class UserMangaList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    manga_id = db.Column(db.Integer, db.ForeignKey('manga.id'), nullable=False)
    list_type = db.Column(db.String(50), nullable=False)  # e.g., 'reading', 'plan_to_read', 'dropped'

    user = db.relationship('User', backref='user_manga_lists')
    manga = db.relationship('Manga', backref='user_manga_lists')
