from app import db

class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manga_id = db.Column(db.Integer)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    score = db.Column(db.Float)
    status = db.Column(db.String(50))
    volumes = db.Column(db.Integer)
    chapters = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    sfw = db.Column(db.Integer)
    genre = db.Column(db.String(50))
    theme = db.Column(db.String(50))
    demographic = db.Column(db.String(25))
    synopsis = db.Column(db.Text)
    image = db.Column(db.String(250))
    url = db.Column(db.String(250))


    def __repr__(self):
        return f'<Manga {self.name}>'

    # Adding the to_dict method
    def to_dict(self):
        return {
            'id': self.id,
            'manga_id': self.manga_id,
            'name': self.name,
            'type': self.type,
            'score': self.score,
            'status': self.status,
            'volumes': self.volumes,
            'chapters': self.chapters,
            'favorites': self.favorites,
            'sfw': self.sfw,
            'genre': self.genre,
            'theme': self.theme,
            'demographic': self.demographic,
            'synopsis': self.synopsis,
            'image': self.image,
            'url': self.url
        }
