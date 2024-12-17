from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

# LoginManager setup
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Sign-up route
@auth_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# Login route
@auth_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        print("Received data:", data)  # Debugging
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        print("Queried user:", user)  # Debugging
        if user and user.check_password(password):
            print("User authenticated!")  # Debugging
            login_user(user)
            return jsonify({"message": "Login successful", "user": user.to_dict()})
        
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print("Error in login route:", str(e))  # Log the error
        return jsonify({"message": "Internal server error"}), 500


# Logout route
@auth_bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})

# Protected route example
@auth_bp.route('/api/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({"message": f"Welcome {current_user.username}!"})
