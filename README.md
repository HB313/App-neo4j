
# 📘 API Flask + Neo4j – Projet TP NoSQL

Ce projet implémente une API RESTful en Python avec Flask, connectée à Neo4j.  
Elle gère les entités suivantes : Utilisateurs, Posts, Commentaires et leurs relations (likes, amitiés, etc.).

---

## ✅ Fonctionnalités

### 👤 Utilisateurs
- CRUD : création, lecture, mise à jour, suppression
- Ajouter / supprimer des amis
- Vérifier amitié entre deux utilisateurs
- Voir amis en commun

### 📝 Posts
- CRUD complet
- Création de post liée à un utilisateur
- Like / unlike d’un post
- Voir qui a liké un post
- Voir nombre total de likes
- Voir les posts d’un utilisateur

### 💬 Commentaires
- CRUD complet
- Création de commentaire liée à un post et un utilisateur
- Like / unlike d’un commentaire
- Voir les commentaires d’un post

---

## ⚙️ Installation & Exécution (Docker)

### 1. Cloner le projet
```bash
git clone <repo_url>
cd app_neo4j
```

### 2. Lancer avec Docker
```bash
docker-compose up --build
```

- API disponible sur : http://localhost:5001
- Interface Neo4j : http://localhost:7474 (login : `neo4j`, password : `password`)

---

## 📁 Arborescence

```
app_neo4j/
├── app/
│   ├── __init__.py
│   ├── routes_users.py
│   ├── routes_posts.py
│   ├── routes_comments.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
├── README.md
└── tests.md
```

---

## 🧪 Tester l’API

Consulte [`tests.md`](tests.md) pour toutes les commandes `curl` ou Postman.

Exemple :

### ➕ Créer un utilisateur
```bash
curl -X POST http://localhost:5001/users/ \
-H "Content-Type: application/json" \
-d '{"name": "Alice", "email": "alice@example.com"}'
```

### ➕ Créer un post
```bash
curl -X POST http://localhost:5001/posts/user/<user_id>/posts \
-H "Content-Type: application/json" \
-d '{"title": "Titre", "content": "Contenu"}'
```

---

## 📚 Technologies

- Python 3.9
- Flask
- py2neo
- Neo4j
- Docker

---

## 🏁 Objectif pédagogique

Ce projet est réalisé dans le cadre d’un TP Ynov sur les bases de données NoSQL et l’utilisation de graphes avec Neo4j.

