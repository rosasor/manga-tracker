# \routes\auth_routes.py

from functools import wraps
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, make_response
from flask_login import login_user, logout_user, login_required
import jwt
from models.user import User
from app import db
import os

# Load environment variables from .env file
load_dotenv()

# Environment-safe SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

auth_bp = Blueprint('auth', __name__)

# JWT decorator for protected routes
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Missing Authorization header"}), 401

        try:
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid or expired token"}), 401
        return f(*args, **kwargs)
    return decorated_function

# Sign-up route
@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# Login route
@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        response = make_response(jsonify({"message": "Login successful", "user": user.to_dict()}))
        return response, 200
    return jsonify({"message": "Invalid credentials"}), 401

# Logout route
@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

# Example protected route
@auth_bp.route('/api/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({"message": f"Welcome {request.user['email']}!"})
