import hashlib
from datetime import datetime


class AuthManager:    
    def __init__(self, db_manager):
        self.db = db_manager
        self.current_user = None
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        password_hash = self.hash_password(password)
        
        query = """
            SELECT id, username, role, nom, prenom, email, actif
            FROM users
            WHERE username = ? AND password_hash = ? AND actif = 1
        """
        
        result = self.db.execute_query(query, (username, password_hash))
        
        if result and len(result) > 0:
            user = dict(result[0])
            self.current_user = user
            
            self.db.execute_update(
                "UPDATE users SET dernier_login = ? WHERE id = ?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user['id'])
            )
            
            self.db.log_action(user['id'], "Connexion réussie", "users", user['id'])
            
            return True, user
        
        return False, None
    
    def logout(self):
        if self.current_user:
            self.db.log_action(self.current_user['id'], "Déconnexion", "users", self.current_user['id'])
            self.current_user = None
    
    def is_authenticated(self):
        return self.current_user is not None
    
    def has_permission(self, action):
        if not self.current_user:
            return False
        
        role = self.current_user.get('role', '')
        
        if role == 'proprietaire':
            return True
        
        if role == 'consultant':
            return action in ['read', 'view', 'export']
        
        return False
    
    def create_user(self, username, password, role, nom=None, prenom=None, email=None):
        if not self.has_permission('create_user'):
            return False, "Permission refusée"
        
        password_hash = self.hash_password(password)
        
        try:
            user_id = self.db.execute_insert("""
                INSERT INTO users (username, password_hash, role, nom, prenom, email, actif)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (username, password_hash, role, nom, prenom, email))
            
            if user_id:
                self.db.log_action(self.current_user['id'], "Création utilisateur", "users", user_id, username)
                return True, "Utilisateur créé avec succès"
            
            return False, "Erreur lors de la création"
        except Exception as e:
            return False, str(e)
    
    def change_password(self, old_password, new_password):
        if not self.current_user:
            return False, "Non authentifié"
        
        old_hash = self.hash_password(old_password)
        
        query = "SELECT id FROM users WHERE id = ? AND password_hash = ?"
        result = self.db.execute_query(query, (self.current_user['id'], old_hash))
        
        if not result:
            return False, "Ancien mot de passe incorrect"
        
        new_hash = self.hash_password(new_password)
        success = self.db.execute_update(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_hash, self.current_user['id'])
        )
        
        if success:
            self.db.log_action(self.current_user['id'], "Changement de mot de passe", "users", self.current_user['id'])
            return True, "Mot de passe modifié avec succès"
        
        return False, "Erreur lors de la modification"
    
    def get_all_users(self):
        if not self.has_permission('view'):
            return []
        
        query = """
            SELECT id, username, role, nom, prenom, email, actif, date_creation, dernier_login
            FROM users
            ORDER BY username
        """
        
        return self.db.execute_query(query)
