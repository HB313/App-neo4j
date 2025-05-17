
# ✅ Fichier de tests - API Flask + Neo4j

Ce fichier contient les cas de test pour vérifier que toutes les routes fonctionnent comme demandé dans le TP.

---

## 👤 Utilisateurs

### ➕ Créer un utilisateur
```bash
curl -X POST http://localhost:5001/users/ -H "Content-Type: application/json" -d '{"name": "Alice", "email": "alice@example.com"}'
```

### 📋 Récupérer tous les utilisateurs
```bash
curl http://localhost:5001/users/
```

### 🔍 Récupérer un utilisateur par ID
```bash
curl http://localhost:5001/users/<user_id>
```

### ✏️ Mettre à jour un utilisateur
```bash
curl -X PUT http://localhost:5001/users/<user_id> -H "Content-Type: application/json" -d '{"name": "Alice Updated", "email": "alice2@example.com"}'
```

### ❌ Supprimer un utilisateur
```bash
curl -X DELETE http://localhost:5001/users/<user_id>
```

### 🤝 Ajouter un ami
```bash
curl -X POST http://localhost:5001/users/<user_id>/friends -H "Content-Type: application/json" -d '{"friend_id": "<friend_id>"}'
```

### 👥 Voir les amis d’un utilisateur
```bash
curl http://localhost:5001/users/<user_id>/friends
```

---

## 📝 Posts

### ➕ Créer un post
```bash
curl -X POST http://localhost:5001/posts/user/<user_id>/posts -H "Content-Type: application/json" -d '{"title": "Titre", "content": "Contenu"}'
```
Les apostrophe et les caractères spéciaux ne sont pas pris en compte.

### 📋 Voir tous les posts
```bash
curl http://localhost:5001/posts/
```

### 🔍 Voir les posts d’un utilisateur
```bash
curl http://localhost:5001/posts/user/<user_id>/posts
```

### ✏️ Modifier un post
```bash
curl -X PUT http://localhost:5001/posts/<post_id> -H "Content-Type: application/json" -d '{"title": "Titre modifié", "content": "Contenu modifié"}'
```

### ❤️ Liker un post
```bash
curl -X POST http://localhost:5001/posts/<post_id>/like -H "Content-Type: application/json" -d '{"user_id": "<user_id>"}'
```

### 🔍 Voir les likes d’un post
bash
```
curl http://localhost:5001/posts/<post_id>/likes
```

### 💔 Unliker un post
```bash
curl -X DELETE http://localhost:5001/posts/<post_id>/like -H "Content-Type: application/json" -d '{"user_id": "<user_id>"}'
```

---

## 💬 Commentaires

### ➕ Ajouter un commentaire à un post
```bash
curl -X POST http://localhost:5001/comments/posts/<post_id>/comments -H "Content-Type: application/json" -d '{"content": "Bravo !", "user_id": "<user_id>"}'
```

### 📋 Voir les commentaires d’un post
```bash
curl http://localhost:5001/comments/posts/<post_id>/comments
```

### ✏️ Modifier un commentaire
```bash
curl -X PUT http://localhost:5001/comments/<comment_id> -H "Content-Type: application/json" -d '{"content": "Commentaire mis à jour"}'
```

### ❌ Supprimer un commentaire
```bash
curl -X DELETE http://localhost:5001/comments/<comment_id>
```

### ❤️ Liker un commentaire
```bash
curl -X POST http://localhost:5001/comments/<comment_id>/like -H "Content-Type: application/json" -d '{"user_id": "<user_id>"}'
```

### 💔 Unliker un commentaire
```bash
curl -X DELETE http://localhost:5001/comments/<comment_id>/like -H "Content-Type: application/json" -d '{"user_id": "<user_id>"}'
```
