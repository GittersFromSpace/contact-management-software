"""Module de gestion des tags et relations"""


class TagManager:
    """Gère les tags personnalisés"""
    
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_tag(self, nom_tag):
        """Crée un nouveau tag"""
        query = "INSERT INTO tags (nom_tag) VALUES (?)"
        
        try:
            tag_id = self.db.execute_insert(query, (nom_tag,))
            if tag_id:
                self.db.log_action(
                    self.auth.current_user['id'],
                    "Création tag",
                    "tags",
                    tag_id,
                    nom_tag
                )
            return tag_id
        except:
            # Tag déjà existant
            return None
    
    def get_all_tags(self):
        """Récupère tous les tags"""
        query = "SELECT * FROM tags ORDER BY nom_tag"
        return self.db.execute_query(query)
    
    def delete_tag(self, tag_id):
        """Supprime un tag"""
        success = self.db.execute_delete("DELETE FROM tags WHERE id = ?", (tag_id,))
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Suppression tag",
                "tags",
                tag_id
            )
        
        return success
    
    def assign_tag_to_contact(self, tag_id, contact_id):
        """Assigne un tag à un contact"""
        query = "INSERT OR IGNORE INTO contact_tags (contact_id, tag_id) VALUES (?, ?)"
        return self.db.execute_insert(query, (contact_id, tag_id))
    
    def remove_tag_from_contact(self, tag_id, contact_id):
        """Retire un tag d'un contact"""
        return self.db.execute_delete(
            "DELETE FROM contact_tags WHERE contact_id = ? AND tag_id = ?",
            (contact_id, tag_id)
        )
    
    def get_contacts_by_tag(self, tag_id):
        """Récupère tous les contacts ayant un tag spécifique"""
        query = """
            SELECT c.*
            FROM contacts c
            JOIN contact_tags ct ON c.id = ct.contact_id
            WHERE ct.tag_id = ?
            ORDER BY c.nom, c.prenom
        """
        return self.db.execute_query(query, (tag_id,))
    
    def get_tags_by_contact(self, contact_id):
        """Récupère tous les tags d'un contact"""
        query = """
            SELECT t.*
            FROM tags t
            JOIN contact_tags ct ON t.id = ct.tag_id
            WHERE ct.contact_id = ?
            ORDER BY t.nom_tag
        """
        return self.db.execute_query(query, (contact_id,))
    
    def count_contacts_by_tag(self, tag_id):
        """Compte le nombre de contacts ayant un tag"""
        query = "SELECT COUNT(*) as count FROM contact_tags WHERE tag_id = ?"
        result = self.db.execute_query(query, (tag_id,))
        return result[0]['count'] if result else 0
    
    def search_contacts_by_tags_and(self, tag_ids):
        """Recherche contacts ayant TOUS les tags (opérateur ET)"""
        if not tag_ids:
            return []
        
        placeholders = ','.join(['?' for _ in tag_ids])
        query = f"""
            SELECT c.*
            FROM contacts c
            WHERE (
                SELECT COUNT(DISTINCT tag_id)
                FROM contact_tags ct
                WHERE ct.contact_id = c.id AND ct.tag_id IN ({placeholders})
            ) = ?
            ORDER BY c.nom, c.prenom
        """
        params = tag_ids + [len(tag_ids)]
        return self.db.execute_query(query, params)
    
    def search_contacts_by_tags_or(self, tag_ids):
        """Recherche contacts ayant AU MOINS UN des tags (opérateur OU)"""
        if not tag_ids:
            return []
        
        placeholders = ','.join(['?' for _ in tag_ids])
        query = f"""
            SELECT DISTINCT c.*
            FROM contacts c
            JOIN contact_tags ct ON c.id = ct.contact_id
            WHERE ct.tag_id IN ({placeholders})
            ORDER BY c.nom, c.prenom
        """
        return self.db.execute_query(query, tag_ids)
    
    def get_contacts_by_tags(self, tag_ids, operator='AND'):
        """Récupère les contacts ayant certains tags"""
        if not tag_ids:
            return []
        
        if operator == 'AND':
            # Tous les tags doivent être présents
            query = f"""
                SELECT c.*
                FROM contacts c
                WHERE (
                    SELECT COUNT(DISTINCT tag_id)
                    FROM contact_tags ct
                    WHERE ct.contact_id = c.id AND ct.tag_id IN ({','.join(['?' for _ in tag_ids])})
                ) = ?
                ORDER BY c.nom, c.prenom
            """
            params = tag_ids + [len(tag_ids)]
        else:  # OR
            # Au moins un tag doit être présent
            query = f"""
                SELECT DISTINCT c.*
                FROM contacts c
                JOIN contact_tags ct ON c.id = ct.contact_id
                WHERE ct.tag_id IN ({','.join(['?' for _ in tag_ids])})
                ORDER BY c.nom, c.prenom
            """
            params = tag_ids
        
        return self.db.execute_query(query, params)
    
    def get_tag_statistics(self):
        """Statistiques sur les tags"""
        query = """
            SELECT t.nom_tag, COUNT(ct.contact_id) as nb_contacts
            FROM tags t
            LEFT JOIN contact_tags ct ON t.id = ct.tag_id
            GROUP BY t.id, t.nom_tag
            ORDER BY nb_contacts DESC, t.nom_tag
        """
        return self.db.execute_query(query)


class RelationManager:
    """Gère les relations entre contacts"""
    
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_relation(self, contact_source_id, contact_cible_id, type_relation):
        """Crée une relation entre deux contacts"""
        query = """
            INSERT INTO relations (contact_source_id, contact_cible_id, type_relation)
            VALUES (?, ?, ?)
        """
        
        relation_id = self.db.execute_insert(query, (contact_source_id, contact_cible_id, type_relation))
        
        if relation_id:
            self.db.log_action(
                self.auth.current_user['id'],
                "Création relation",
                "relations",
                relation_id,
                f"{contact_source_id} -> {contact_cible_id}: {type_relation}"
            )
        
        return relation_id
    
    def get_relations(self, contact_id=None):
        """Récupère les relations (toutes ou pour un contact)"""
        if contact_id:
            query = """
                SELECT r.*,
                       cs.nom as nom_source, cs.prenom as prenom_source,
                       cc.nom as nom_cible, cc.prenom as prenom_cible
                FROM relations r
                JOIN contacts cs ON r.contact_source_id = cs.id
                JOIN contacts cc ON r.contact_cible_id = cc.id
                WHERE r.contact_source_id = ? OR r.contact_cible_id = ?
                ORDER BY r.date_creation DESC
            """
            params = (contact_id, contact_id)
        else:
            query = """
                SELECT r.*,
                       cs.nom as nom_source, cs.prenom as prenom_source,
                       cc.nom as nom_cible, cc.prenom as prenom_cible
                FROM relations r
                JOIN contacts cs ON r.contact_source_id = cs.id
                JOIN contacts cc ON r.contact_cible_id = cc.id
                ORDER BY r.date_creation DESC
            """
            params = None
        
        return self.db.execute_query(query, params)
    
    def get_all_relations(self):
        """Récupère toutes les relations avec noms complets"""
        query = """
            SELECT r.*,
                   cs.nom as source_nom, cs.prenom as source_prenom,
                   cc.nom as cible_nom, cc.prenom as cible_prenom
            FROM relations r
            JOIN contacts cs ON r.contact_source_id = cs.id
            JOIN contacts cc ON r.contact_cible_id = cc.id
            ORDER BY r.date_creation DESC
        """
        return self.db.execute_query(query)
    
    def delete_relation(self, relation_id):
        """Supprime une relation"""
        success = self.db.execute_delete("DELETE FROM relations WHERE id = ?", (relation_id,))
        
        if success:
            self.db.log_action(
                self.auth.current_user['id'],
                "Suppression relation",
                "relations",
                relation_id
            )
        
        return success
    
    def get_relation_types(self):
        """Récupère les types de relations distincts"""
        query = "SELECT DISTINCT type_relation FROM relations WHERE type_relation IS NOT NULL ORDER BY type_relation"
        result = self.db.execute_query(query)
        return [row['type_relation'] for row in result] if result else []
    
    def get_network_data(self):
        """Récupère les données pour visualisation du réseau"""
        # Récupère tous les contacts et relations pour créer un graphe
        contacts = self.db.execute_query("SELECT id, nom, prenom FROM contacts")
        relations = self.get_relations()
        
        return {
            'contacts': contacts,
            'relations': relations
        }
