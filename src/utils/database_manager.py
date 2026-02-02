import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Utiliser le chemin absolu vers la racine du projet
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(project_root, "data", "app.db")
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.initialize_database()
    
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return False
    
    def initialize_database(self):
        script_path = os.path.join(os.path.dirname(__file__), '../../data/001_CREATE_TABLES.sql')
        
        if os.path.exists(script_path):
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()
            except Exception as e:
                print(f"Erreur lors de l'initialisation de la base de données: {e}")
        
        self.create_settings_table()
        self.create_default_user()
    
    def create_settings_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS app_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
        except Exception as e:
            print(f"Erreur lors de la création de la table settings: {e}")
    
    def get_setting(self, key, default=None):
        try:
            self.cursor.execute("SELECT value FROM app_settings WHERE key = ?", (key,))
            result = self.cursor.fetchone()
            return result[0] if result else default
        except Exception:
            return default
    
    def set_setting(self, key, value):
        try:
            self.cursor.execute("""
                INSERT INTO app_settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET 
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, value))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du paramètre: {e}")
            return False
    
    def create_default_user(self):
        import hashlib
        
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                # Mot de passe par défaut: "admin"
                password_hash = hashlib.sha256("admin".encode()).hexdigest()
                self.cursor.execute("""
                    INSERT INTO users (username, password_hash, role, nom, prenom, email, actif)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, ("admin", password_hash, "proprietaire", "Admin", "System", "admin@contact-app.com", 1))
                self.connection.commit()
                print("Utilisateur par défaut créé (username: admin, password: admin)")
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur par défaut: {e}")
    
    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur d'exécution de la requête: {e}")
            return None
    
    def execute_insert(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur d'insertion: {e}")
            self.connection.rollback()
            return None
    
    def execute_update(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erreur de mise à jour: {e}")
            self.connection.rollback()
            return False
    
    def execute_delete(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erreur de suppression: {e}")
            self.connection.rollback()
            return False
    
    def log_action(self, user_id, action, table_cible=None, cible_id=None, details=None):
        try:
            self.cursor.execute("""
                INSERT INTO logs (user_id, action, table_cible, cible_id, details)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, action, table_cible, cible_id, details))
            self.connection.commit()
        except Exception as e:
            print(f"Erreur lors de l'enregistrement du log: {e}")
    
    def backup_database(self, backup_path=None):
        import shutil
        from datetime import datetime
        
        if backup_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_contacts_{timestamp}.db"
        
        try:
            shutil.copy2(self.db_path, backup_path)
            return True, backup_path
        except Exception as e:
            return False, str(e)
    
    def close(self):
        if self.connection:
            self.connection.close()
