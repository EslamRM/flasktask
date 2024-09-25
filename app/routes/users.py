from flask import Blueprint, request, jsonify
from app.database import get_db
from app.services.user_service import UserService

user_bp = Blueprint('users', __name__)

def get_user_service():
    db = get_db()
    return UserService(db)

@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password_hash = data.get('password_hash')
    user_id = get_user_service().create_user(name, email, password_hash)
    return jsonify({'user_id': user_id}), 201

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_service().get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404
