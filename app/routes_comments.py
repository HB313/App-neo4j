# app/routes_comments.py
from flask import Blueprint, request, jsonify
from py2neo import Node
from app import graph
import uuid, datetime

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

def now(): return str(datetime.datetime.utcnow())
def generate_id(): return str(uuid.uuid4())

@comments_bp.route('/', methods=['GET'])
def get_comments():
    comments = graph.run("MATCH (c:Comment) RETURN c").data()
    return jsonify([dict(c['c']) for c in comments])

@comments_bp.route('/<comment_id>', methods=['GET'])
def get_comment_by_id(comment_id):
    result = graph.run("MATCH (c:Comment {id: $id}) RETURN c", id=comment_id).data()
    if not result:
        return jsonify({'error': 'Commentaire non trouvé'}), 404
    return jsonify(dict(result[0]['c']))

@comments_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.get_json()
    query = '''
        MATCH (c:Comment {id: $id})
        SET c.content = $content
        RETURN c
    '''
    result = graph.run(query, id=comment_id, content=data['content']).data()
    if not result:
        return jsonify({'error': 'Commentaire non trouvé'}), 404
    return jsonify(dict(result[0]['c']))

@comments_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    graph.run("MATCH (c:Comment {id: $id}) DETACH DELETE c", id=comment_id)
    return jsonify({'message': 'Commentaire supprimé'})

@comments_bp.route('/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    data = request.get_json()
    query = '''
        MATCH (u:User {id: $user_id}), (c:Comment {id: $comment_id})
        MERGE (u)-[:LIKES]->(c)
    '''
    graph.run(query, user_id=data['user_id'], comment_id=comment_id)
    return jsonify({'message': 'Commentaire liké'})

@comments_bp.route('/<comment_id>/like', methods=['DELETE'])
def unlike_comment(comment_id):
    data = request.get_json()
    query = '''
        MATCH (u:User {id: $user_id})-[r:LIKES]->(c:Comment {id: $comment_id})
        DELETE r
    '''
    graph.run(query, user_id=data['user_id'], comment_id=comment_id)
    return jsonify({'message': 'Like retiré'})

# Route pour lier un commentaire à un post
from flask import current_app as app

@comments_bp.route('/posts/<post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    cid = generate_id()
    graph.run('''
        MATCH (u:User {id: $user_id}), (p:Post {id: $post_id})
        CREATE (c:Comment {id: $cid, content: $content, created_at: $created_at})
        CREATE (u)-[:CREATED]->(c)
        CREATE (p)-[:HAS_COMMENT]->(c)
    ''', user_id=data['user_id'], post_id=post_id, cid=cid, content=data['content'], created_at=now())
    return jsonify({'message': 'Commentaire créé', 'comment_id': cid}), 201

@comments_bp.route('/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    result = graph.run('''
        MATCH (p:Post {id: $post_id})-[:HAS_COMMENT]->(c:Comment)
        RETURN c
    ''', post_id=post_id).data()
    return jsonify([dict(r['c']) for r in result])

@comments_bp.route('/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_post_comment(post_id, comment_id):
    query = '''
        MATCH (p:Post {id: $post_id})-[r:HAS_COMMENT]->(c:Comment {id: $comment_id})
        DELETE r
    '''
    graph.run(query, post_id=post_id, comment_id=comment_id)
    graph.run("MATCH (c:Comment {id: $id}) DETACH DELETE c", id=comment_id)
    return jsonify({'message': 'Commentaire supprimé du post'})