# app/routes_posts.py
from flask import Blueprint, request, jsonify
from py2neo import Node
from app import graph
import uuid, datetime

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

def now(): return str(datetime.datetime.utcnow())
def generate_id(): return str(uuid.uuid4())

@posts_bp.route('/', methods=['GET'])
def get_posts():
    posts = graph.run("MATCH (p:Post) RETURN p").data()
    return jsonify([dict(p['p']) for p in posts])

@posts_bp.route('/<post_id>', methods=['GET'])
def get_post_by_id(post_id):
    result = graph.run("MATCH (p:Post {id: $id}) RETURN p", id=post_id).data()
    if not result:
        return jsonify({'error': 'Post non trouvé'}), 404
    return jsonify(dict(result[0]['p']))

@posts_bp.route('/<post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    query = """
        MATCH (p:Post {id: $id})
        SET p.title = $title, p.content = $content
        RETURN p
    """
    result = graph.run(query, id=post_id, title=data['title'], content=data['content']).data()
    if not result:
        return jsonify({'error': 'Post non trouvé'}), 404
    return jsonify(dict(result[0]['p']))

@posts_bp.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    graph.run("MATCH (p:Post {id: $id}) DETACH DELETE p", id=post_id)
    return jsonify({'message': 'Post supprimé'})

@posts_bp.route('/<post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.get_json()
    query = '''
        MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
        MERGE (u)-[:LIKES]->(p)
    '''
    graph.run(query, user_id=data['user_id'], post_id=post_id)
    return jsonify({'message': 'Post liké'})

@posts_bp.route('/<post_id>/like', methods=['DELETE'])
def unlike_post(post_id):
    data = request.get_json()
    query = '''
        MATCH (u:User {id: $user_id})-[r:LIKES]->(p:Post {id: $post_id})
        DELETE r
    '''
    graph.run(query, user_id=data['user_id'], post_id=post_id)
    return jsonify({'message': 'Like retiré'})

@posts_bp.route('/user/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    query = '''
        MATCH (u:User {id: $id})-[:CREATED]->(p:Post)
        RETURN p
    '''
    result = graph.run(query, id=user_id).data()
    return jsonify([dict(r['p']) for r in result])

@posts_bp.route('/user/<user_id>/posts', methods=['POST'])
def create_post(user_id):
    data = request.get_json()
    pid = generate_id()
    graph.run('''
        MATCH (u:User {id: $user_id})
        CREATE (p:Post {id: $pid, title: $title, content: $content, created_at: $created_at})
        CREATE (u)-[:CREATED]->(p)
    ''', user_id=user_id, pid=pid, title=data['title'], content=data['content'], created_at=now())
    return jsonify({'message': 'Post créé', 'post_id': pid}), 201

@posts_bp.route('/<post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    result = graph.run("""
        MATCH (u:User)-[:LIKES]->(p:Post {id: $id})
        RETURN u
    """, id=post_id).data()
    return jsonify([dict(r['u']) for r in result])

@posts_bp.route('/<post_id>/likes/count', methods=['GET'])
def count_post_likes(post_id):
    result = graph.run("""
        MATCH (u:User)-[:LIKES]->(p:Post {id: $id})
        RETURN count(u) AS likes
    """, id=post_id).data()
    return jsonify({'like_count': result[0]['likes']})