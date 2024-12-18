# \app.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize db
db = SQLAlchemy()

def create_app():
    # Initialize the app
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/elena/Coding Projects/manga-python/data/mangaMAL.db?check_same_thread=False'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db with app
    db.init_app(app)

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models.user import User
    # Define user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import blueprint and register it after app creation
    from routes.auth_routes import auth_bp
    from routes.manga_routes import manga_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(manga_bp)

    return app
