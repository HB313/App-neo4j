# app/__init__.py
from flask import Flask
from py2neo import Graph

graph = None

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True

    global graph
    graph = Graph("bolt://neo4j:7687", auth=("neo4j", "password"))

    from .routes_users import users_bp
    from .routes_posts import posts_bp
    from .routes_comments import comments_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)

    print("✅ Flask app et connexion Neo4j initialisées")
    return app
