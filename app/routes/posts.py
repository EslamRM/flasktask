from flask import Blueprint, request, jsonify
from app.database import get_db
from app.services.post_service import PostService

post_bp = Blueprint('posts', __name__)

def get_post_service():
    db = get_db()
    return PostService(db)

@post_bp.route('/post', methods=['POST'])
def create_post():
    data = request.json
    user_id = data.get('user_id')
    content = data.get('content')
    post_id = get_post_service().create_post(user_id, content)
    return jsonify({'post_id': post_id}), 201

@post_bp.route('/post/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    content = request.json.get('content')
    get_post_service().update_post(post_id, content)
    return '', 204

@post_bp.route('/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    get_post_service().delete_post(post_id)
    return '', 204

@post_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = get_post_service().get_post(post_id)
    if post:
        return jsonify(post)
    return jsonify({'error': 'Post not found'}), 404

@post_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = get_post_service().get_all_posts()
    return jsonify(posts), 200
