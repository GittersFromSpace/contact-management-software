"""Module de gestion des interactions"""
from datetime import datetime


class InteractionManager:
    """Gère les interactions avec les contacts"""
    
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_interaction(self, contact_id, type_interaction, description, statut='', date_heure=None):
        """Crée une nouvelle interaction"""
        if date_heure is None:
            date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
            INSERT INTO interactions (contact_id, type_interaction, date_heure, description, statut)
            VALUES (?, ?, ?, ?, ?)
        """
        
        interaction_id = self.db.execute_insert(
            query,
            (contact_id, type_interaction, date_heure, description, statut)
        )
        
        if interaction_id:
            self.db.log_action(
                self.auth.current_user['id'],
                "Création interaction",
                "interactions",
                interaction_id,
                f"Contact {contact_id} - {type_interaction}"
            )
        
        return interaction_id
    
    def get_interactions(self, contact_id=None, limit=None):
        """Récupère les interactions (toutes ou pour un contact)"""
        if contact_id:
            query = """
                SELECT i.*, c.nom, c.prenom
                FROM interactions i
                JOIN contacts c ON i.contact_id = c.id
                WHERE i.contact_id = ?
                ORDER BY i.date_heure DESC
            """
            params = (contact_id,)
        else:
            query = """
                SELECT i.*, c.nom, c.prenom
                FROM interactions i
                JOIN contacts c ON i.contact_id = c.id
                ORDER BY i.date_heure DESC
            """
            params = None
        
        if limit:
            query += f" LIMIT {limit}"
        
        return self.db.execute_query(query, params)
    
    def delete_interaction(self, interaction_id):
        """Supprime une interaction"""
        success = self.db.execute_delete("DELETE FROM interactions WHERE id = ?", (interaction_id,))
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Suppression interaction",
                "interactions",
                interaction_id
            )
        
        return success
    
    def search_interactions(self, search_text='', type_interaction='', date_debut='', date_fin=''):
        """Recherche des interactions avec filtres"""
        query = """
            SELECT i.*, c.nom, c.prenom
            FROM interactions i
            JOIN contacts c ON i.contact_id = c.id
            WHERE 1=1
        """
        params = []
        
        if search_text:
            query += " AND (i.description LIKE ? OR c.nom LIKE ? OR c.prenom LIKE ?)"
            search_term = f"%{search_text}%"
            params.extend([search_term, search_term, search_term])
        
        if type_interaction:
            query += " AND i.type_interaction = ?"
            params.append(type_interaction)
        
        if date_debut:
            query += " AND DATE(i.date_heure) >= ?"
            params.append(date_debut)
        
        if date_fin:
            query += " AND DATE(i.date_heure) <= ?"
            params.append(date_fin)
        
        query += " ORDER BY i.date_heure DESC"
        
        return self.db.execute_query(query, params if params else None)
    
    def get_interaction_types(self):
        """Récupère les types d'interactions distincts"""
        query = "SELECT DISTINCT type_interaction FROM interactions WHERE type_interaction IS NOT NULL ORDER BY type_interaction"
        result = self.db.execute_query(query)
        return [row['type_interaction'] for row in result] if result else []
    
    def add_piece_jointe(self, contact_id, interaction_id, chemin_fichier, description=''):
        """Ajoute une pièce jointe"""
        query = """
            INSERT INTO pieces_jointes (contact_id, interaction_id, chemin_fichier, description)
            VALUES (?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (contact_id, interaction_id, chemin_fichier, description))
    
    def get_pieces_jointes(self, contact_id=None, interaction_id=None):
        """Récupère les pièces jointes"""
        query = "SELECT * FROM pieces_jointes WHERE 1=1"
        params = []
        
        if contact_id:
            query += " AND contact_id = ?"
            params.append(contact_id)
        
        if interaction_id:
            query += " AND interaction_id = ?"
            params.append(interaction_id)
        
        query += " ORDER BY date_ajout DESC"
        
        return self.db.execute_query(query, params if params else None)


class RappelManager:
    """Gère les rappels et anniversaires"""
    
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_rappel(self, contact_id, titre, date_heure, type_rappel='', description='', priorite='moyenne', repetition=''):
        """Crée un nouveau rappel"""
        query = """
            INSERT INTO rappels (contact_id, type_rappel, titre, date_heure, description, priorite, repetition, traite)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """
        
        rappel_id = self.db.execute_insert(
            query,
            (contact_id, type_rappel, titre, date_heure, description, priorite, repetition)
        )
        
        if rappel_id:
            self.db.log_action(
                self.auth.current_user['id'],
                "Création rappel",
                "rappels",
                rappel_id,
                titre
            )
        
        return rappel_id
    
    def get_rappels(self, contact_id=None, traite=None, jours_futur=None):
        """Récupère les rappels"""
        query = """
            SELECT r.*, c.nom, c.prenom
            FROM rappels r
            JOIN contacts c ON r.contact_id = c.id
            WHERE 1=1
        """
        params = []
        
        if contact_id:
            query += " AND r.contact_id = ?"
            params.append(contact_id)
        
        if traite is not None:
            query += " AND r.traite = ?"
            params.append(traite)
        
        if jours_futur:
            query += " AND DATE(r.date_heure) >= DATE('now') AND DATE(r.date_heure) <= DATE('now', ?)"
            params.append(f'+{jours_futur} days')
        
        query += " ORDER BY r.date_heure ASC"
        
        return self.db.execute_query(query, params if params else None)
    
    def marquer_traite(self, rappel_id):
        """Marque un rappel comme traité"""
        success = self.db.execute_update("UPDATE rappels SET traite = 1 WHERE id = ?", (rappel_id,))
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Rappel traité",
                "rappels",
                rappel_id
            )
        
        return success
    
    def delete_rappel(self, rappel_id):
        """Supprime un rappel"""
        success = self.db.execute_delete("DELETE FROM rappels WHERE id = ?", (rappel_id,))
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Suppression rappel",
                "rappels",
                rappel_id
            )
        
        return success
    
    def get_rappels_aujourdhui(self):
        """Récupère les rappels d'aujourd'hui non traités"""
        query = """
            SELECT r.*, c.nom, c.prenom
            FROM rappels r
            JOIN contacts c ON r.contact_id = c.id
            WHERE r.traite = 0 AND DATE(r.date_heure) = DATE('now')
            ORDER BY r.date_heure ASC
        """
        return self.db.execute_query(query)
    
    def get_anniversaires_proches(self, jours=30):
        """Récupère les anniversaires à venir"""
        # Cette requête est simplifiée - dans une vraie app, il faudrait gérer le changement d'année
        query = """
            SELECT id, nom, prenom, date_naissance
            FROM contacts
            WHERE date_naissance IS NOT NULL AND date_naissance != ''
            ORDER BY date_naissance
        """
        return self.db.execute_query(query)
