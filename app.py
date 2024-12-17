import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize db
db = SQLAlchemy()

def create_app():
    # Initialize the app
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    # CORS(app, origins=["http://localhost:3000"])  # Only allow requests from your Next.js frontend


    # Configuration
    app.config['SECRET_KEY'] = os.urandom(24)  # Random secret key
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/mangaMAL.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/elena/Coding Projects/manga-python/data/mangaMAL.db?check_same_thread=False'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    db.init_app(app)

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Import blueprint and register it after app creation
    from routes.manga_routes import manga_bp
    app.register_blueprint(manga_bp)

    from routes.auth_routes import auth_bp
    # Import the User model to ensure it is registered with SQLAlchemy
    from models.user import User  # Make sure this is in app.py

    app.register_blueprint(auth_bp)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
