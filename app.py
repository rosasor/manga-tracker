from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Initialize db
db = SQLAlchemy()

def create_app():
    # Initialize the app
    app = Flask(__name__)

    # Database configuration
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/mangaMAL.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/elena/Coding Projects/manga-python/data/mangaMAL.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    db.init_app(app)

    # Import blueprint and register it after app creation
    from routes.manga_routes import manga_bp
    app.register_blueprint(manga_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
