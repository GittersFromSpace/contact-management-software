"""Module de gestion des tâches et projets"""
from datetime import datetime


class TaskManager:
    """Gère les tâches liées aux contacts"""
    
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_task(self, titre, description, contact_ids, priorite='moyenne', statut='A faire', date_echeance=None, projet_id=None):
        """Crée une nouvelle tâche"""
        if not contact_ids or len(contact_ids) == 0:
            return False, "Au moins un contact doit être sélectionné"
        
        query = """
            INSERT INTO taches (titre, description, date_echeance, priorite, statut, projet_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        
        task_id = self.db.execute_insert(
            query,
            (titre, description, date_echeance, priorite, statut, projet_id)
        )
        
        if task_id:
            # Associer les contacts à la tâche
            for contact_id in contact_ids:
                self.db.execute_insert(
                    "INSERT INTO tache_contacts (tache_id, contact_id) VALUES (?, ?)",
                    (task_id, contact_id)
                )
            
            self.db.log_action(
                self.auth.current_user['id'],
                "Création tâche",
                "taches",
                task_id,
                titre
            )
            
            return True, task_id
        
        return False, None
    
    def update_task(self, task_id, titre, description, priorite, statut, date_echeance, projet_id=None):
        """Met à jour une tâche"""
        query = """
            UPDATE taches SET
                titre = ?, description = ?, date_echeance = ?, priorite = ?,
                statut = ?, projet_id = ?, date_modification = ?
            WHERE id = ?
        """
        
        success = self.db.execute_update(
            query,
            (titre, description, date_echeance, priorite, statut, projet_id,
             datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id)
        )
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Modification tâche",
                "taches",
                task_id
            )
        
        return success
    
    def delete_task(self, task_id):
        """Supprime une tâche"""
        success = self.db.execute_delete("DELETE FROM taches WHERE id = ?", (task_id,))
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Suppression tâche",
                "taches",
                task_id
            )
        
        return success
    
    def get_task(self, task_id):
        """Récupère une tâche avec ses contacts associés"""
        query = "SELECT * FROM taches WHERE id = ?"
        result = self.db.execute_query(query, (task_id,))
        
        if result and len(result) > 0:
            task = dict(result[0])
            
            # Récupérer les contacts associés
            contacts_query = """
                SELECT c.id, c.nom, c.prenom, c.societe
                FROM contacts c
                JOIN tache_contacts tc ON c.id = tc.contact_id
                WHERE tc.tache_id = ?
            """
            task['contacts'] = self.db.execute_query(contacts_query, (task_id,))
            
            return task
        
        return None
    
    def get_tasks(self, filters=None):
        """Récupère les tâches avec filtres optionnels"""
        query = """
            SELECT DISTINCT t.*
            FROM taches t
            LEFT JOIN tache_contacts tc ON t.id = tc.tache_id
            WHERE 1=1
        """
        params = []
        
        if filters:
            if filters.get('contact_id'):
                query += " AND tc.contact_id = ?"
                params.append(filters['contact_id'])
            
            if filters.get('priorite'):
                query += " AND t.priorite = ?"
                params.append(filters['priorite'])
            
            if filters.get('statut'):
                query += " AND t.statut = ?"
                params.append(filters['statut'])
            
            if filters.get('projet_id'):
                query += " AND t.projet_id = ?"
                params.append(filters['projet_id'])
            
            if filters.get('echeance'):
                if filters['echeance'] == 'aujourdhui':
                    query += " AND DATE(t.date_echeance) = DATE('now')"
                elif filters['echeance'] == 'semaine':
                    query += " AND DATE(t.date_echeance) BETWEEN DATE('now') AND DATE('now', '+7 days')"
                elif filters['echeance'] == 'mois':
                    query += " AND DATE(t.date_echeance) BETWEEN DATE('now') AND DATE('now', '+30 days')"
        
        query += " ORDER BY t.date_echeance ASC, t.priorite DESC"
        
        return self.db.execute_query(query, params if params else None)
    
    def marquer_terminee(self, task_id):
        """Marque une tâche comme terminée"""
        return self.db.execute_update("UPDATE taches SET statut = 'Terminé' WHERE id = ?", (task_id,))
    
    def get_task_contacts(self, task_id):
        """Récupère les contacts d'une tâche"""
        query = """
            SELECT c.id, c.nom, c.prenom, c.societe
            FROM contacts c
            JOIN tache_contacts tc ON c.id = tc.contact_id
            WHERE tc.tache_id = ?
        """
        return self.db.execute_query(query, (task_id,))
    
    def get_tasks_by_projet(self, projet_id):
        """Récupère toutes les tâches d'un projet"""
        query = "SELECT * FROM taches WHERE projet_id = ? ORDER BY date_echeance"
        return self.db.execute_query(query, (projet_id,))
    
    def assign_task_to_projet(self, task_id, projet_id):
        """Assigne une tâche à un projet (ou la retire si projet_id est None)"""
        query = "UPDATE taches SET projet_id = ? WHERE id = ?"
        return self.db.execute_update(query, (projet_id, task_id))


class ProjetManager:
    """Gère les projets"""
    
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_projet(self, nom, description='', objectif='', date_debut=None, date_fin_previsionnelle=None):
        """Crée un nouveau projet"""
        query = """
            INSERT INTO projets (nom, description, objectif, date_debut, date_fin_previsionnelle)
            VALUES (?, ?, ?, ?, ?)
        """
        
        projet_id = self.db.execute_insert(
            query,
            (nom, description, objectif, date_debut, date_fin_previsionnelle)
        )
        
        if projet_id:
            self.db.log_action(
                self.auth.current_user['id'],
                "Création projet",
                "projets",
                projet_id,
                nom
            )
        
        return projet_id
    
    def update_projet(self, projet_id, nom, description, objectif, date_debut, date_fin_previsionnelle):
        """Met à jour un projet"""
        query = """
            UPDATE projets SET
                nom = ?, description = ?, objectif = ?, date_debut = ?, date_fin_previsionnelle = ?
            WHERE id = ?
        """
        
        success = self.db.execute_update(
            query,
            (nom, description, objectif, date_debut, date_fin_previsionnelle, projet_id)
        )
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Modification projet",
                "projets",
                projet_id
            )
        
        return success
    
    def delete_projet(self, projet_id):
        """Supprime un projet"""
        # Les tâches associées auront leur projet_id mis à NULL (ON DELETE SET NULL)
        success = self.db.execute_delete("DELETE FROM projets WHERE id = ?", (projet_id,))
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Suppression projet",
                "projets",
                projet_id
            )
        
        return success
    
    def get_projet(self, projet_id):
        """Récupère un projet avec ses statistiques"""
        query = "SELECT * FROM projets WHERE id = ?"
        result = self.db.execute_query(query, (projet_id,))
        
        if result and len(result) > 0:
            projet = dict(result[0])
            
            # Statistiques du projet
            stats_query = """
                SELECT
                    COUNT(*) as total_taches,
                    SUM(CASE WHEN statut = 'Terminé' THEN 1 ELSE 0 END) as taches_terminees,
                    SUM(CASE WHEN statut = 'En cours' THEN 1 ELSE 0 END) as taches_en_cours,
                    SUM(CASE WHEN statut = 'A faire' THEN 1 ELSE 0 END) as taches_a_faire
                FROM taches
                WHERE projet_id = ?
            """
            stats = self.db.execute_query(stats_query, (projet_id,))
            
            if stats and len(stats) > 0:
                projet['stats'] = dict(stats[0])
                # Calcul du pourcentage d'avancement
                total = projet['stats']['total_taches']
                if total > 0:
                    projet['stats']['avancement'] = (projet['stats']['taches_terminees'] / total) * 100
                else:
                    projet['stats']['avancement'] = 0
            
            # Contacts impliqués
            contacts_query = """
                SELECT DISTINCT c.id, c.nom, c.prenom, c.societe
                FROM contacts c
                JOIN tache_contacts tc ON c.id = tc.contact_id
                JOIN taches t ON tc.tache_id = t.id
                WHERE t.projet_id = ?
            """
            projet['contacts'] = self.db.execute_query(contacts_query, (projet_id,))
            
            return projet
        
        return None
    
    def get_all_projets(self):
        """Récupère tous les projets"""
        query = "SELECT * FROM projets ORDER BY date_creation DESC"
        return self.db.execute_query(query)
    
    def get_projet_by_id(self, projet_id):
        """Récupère un projet par son ID"""
        query = "SELECT * FROM projets WHERE id = ?"
        result = self.db.execute_query(query, (projet_id,))
        if result and len(result) > 0:
            return dict(result[0])
        return None
    
    def get_projet_tasks(self, projet_id):
        """Récupère toutes les tâches d'un projet"""
        query = "SELECT * FROM taches WHERE projet_id = ? ORDER BY date_echeance"
        return self.db.execute_query(query, (projet_id,))
