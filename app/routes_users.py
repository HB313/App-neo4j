# app/routes_users.py
from flask import Blueprint, request, jsonify
from py2neo import Node, Relationship
from app import graph
import uuid, datetime

users_bp = Blueprint('users', __name__, url_prefix='/users')

def now(): return str(datetime.datetime.utcnow())
def generate_id(): return str(uuid.uuid4())

@users_bp.route('/', methods=['GET'])
def get_users():
    users = graph.run("MATCH (u:User) RETURN u").data()
    return jsonify([dict(u['u']) for u in users])

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = Node("User", id=generate_id(), name=data['name'], email=data['email'], created_at=now())
    graph.create(user)
    return jsonify(dict(user)), 201

@users_bp.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    result = graph.run("MATCH (u:User {id: $id}) RETURN u", id=user_id).data()
    if not result:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    return jsonify(dict(result[0]['u']))

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    query = """
        MATCH (u:User {id: $id})
        SET u.name = $name, u.email = $email
        RETURN u
    """
    result = graph.run(query, id=user_id, name=data['name'], email=data['email']).data()
    if not result:
        return jsonify({'error': 'Utilisateur non trouvé'}), 404
    return jsonify(dict(result[0]['u']))

@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    graph.run("MATCH (u:User {id: $id}) DETACH DELETE u", id=user_id)
    return jsonify({'message': 'Utilisateur supprimé'})

@users_bp.route('/<user_id>/friends', methods=['POST'])
def add_friend(user_id):
    data = request.get_json()
    query = '''
        MATCH (u1:User {id: $user_id}), (u2:User {id: $friend_id})
        MERGE (u1)-[:FRIENDS_WITH]->(u2)
        MERGE (u2)-[:FRIENDS_WITH]->(u1)
    '''
    graph.run(query, user_id=user_id, friend_id=data['friend_id'])
    return jsonify({'message': 'Ami ajouté'})

@users_bp.route('/<user_id>/friends', methods=['GET'])
def get_friends(user_id):
    query = '''
        MATCH (u:User {id: $id})-[:FRIENDS_WITH]->(f:User)
        RETURN f
    '''
    result = graph.run(query, id=user_id).data()
    return jsonify([dict(r['f']) for r in result])

@users_bp.route('/<user_id>/friends/<friend_id>', methods=['DELETE'])
def remove_friend(user_id, friend_id):
    query = '''
        MATCH (u1:User {id: $user_id})-[r:FRIENDS_WITH]-(u2:User {id: $friend_id})
        DELETE r
    '''
    graph.run(query, user_id=user_id, friend_id=friend_id)
    return jsonify({'message': 'Ami supprimé'})

@users_bp.route('/<user_id>/friends/<friend_id>', methods=['GET'])
def check_friendship(user_id, friend_id):
    query = '''
        MATCH (u1:User {id: $user_id})-[:FRIENDS_WITH]-(u2:User {id: $friend_id})
        RETURN u2
    '''
    result = graph.run(query, user_id=user_id, friend_id=friend_id).data()
    return jsonify({'friends': bool(result)})

@users_bp.route('/<user_id>/mutual-friends/<other_id>', methods=['GET'])
def get_mutual_friends(user_id, other_id):
    query = '''
        MATCH (a:User {id: $user_id})-[:FRIENDS_WITH]->(f:User)<-[:FRIENDS_WITH]-(b:User {id: $other_id})
        RETURN f
    '''
    result = graph.run(query, user_id=user_id, other_id=other_id).data()
    return jsonify([dict(r['f']) for r in result])
