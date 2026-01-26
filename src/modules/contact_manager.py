"""Module de gestion des contacts"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os


class ContactManager:
    """Gère toutes les opérations sur les contacts"""
    
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_contact(self, contact_data):
        """Crée un nouveau contact"""
        try:
            query = """
                INSERT INTO contacts (
                    civilite, nom, prenom, societe, poste, categorie,
                    photo_path, date_naissance, anniversaire_professionnel,
                    site_web, adresse_rue, adresse_code_postal, adresse_ville, adresse_pays,
                    date_modification
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                contact_data.get('civilite', ''),
                contact_data.get('nom', ''),
                contact_data.get('prenom', ''),
                contact_data.get('societe', ''),
                contact_data.get('poste', ''),
                contact_data.get('categorie', ''),
                contact_data.get('photo_path', ''),
                contact_data.get('date_naissance', ''),
                contact_data.get('anniversaire_professionnel', ''),
                contact_data.get('site_web', ''),
                contact_data.get('adresse_rue', ''),
                contact_data.get('adresse_code_postal', ''),
                contact_data.get('adresse_ville', ''),
                contact_data.get('adresse_pays', ''),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            contact_id = self.db.execute_insert(query, params)
            
            if contact_id:
                # Ajouter les coordonnées (téléphones, emails)
                if 'coordonnees' in contact_data:
                    for coord in contact_data['coordonnees']:
                        self.add_coordonnee(contact_id, coord['type'], coord['valeur'], coord.get('principal', 0))
                
                # Ajouter les réseaux sociaux
                if 'reseaux_sociaux' in contact_data:
                    for reseau in contact_data['reseaux_sociaux']:
                        self.add_reseau_social(contact_id, reseau['plateforme'], reseau['url'])
                
                # Log
                self.db.log_action(
                    self.auth.current_user['id'],
                    "Création contact",
                    "contacts",
                    contact_id,
                    f"{contact_data.get('prenom', '')} {contact_data.get('nom', '')}"
                )
                
                return True, contact_id
            
            return False, None
        except Exception as e:
            print(f"Erreur création contact: {e}")
            return False, None
    
    def update_contact(self, contact_id, contact_data):
        """Met à jour un contact existant"""
        try:
            query = """
                UPDATE contacts SET
                    civilite = ?, nom = ?, prenom = ?, societe = ?, poste = ?, categorie = ?,
                    photo_path = ?, date_naissance = ?, anniversaire_professionnel = ?,
                    site_web = ?, adresse_rue = ?, adresse_code_postal = ?, adresse_ville = ?,
                    adresse_pays = ?, date_modification = ?
                WHERE id = ?
            """
            
            params = (
                contact_data.get('civilite', ''),
                contact_data.get('nom', ''),
                contact_data.get('prenom', ''),
                contact_data.get('societe', ''),
                contact_data.get('poste', ''),
                contact_data.get('categorie', ''),
                contact_data.get('photo_path', ''),
                contact_data.get('date_naissance', ''),
                contact_data.get('anniversaire_professionnel', ''),
                contact_data.get('site_web', ''),
                contact_data.get('adresse_rue', ''),
                contact_data.get('adresse_code_postal', ''),
                contact_data.get('adresse_ville', ''),
                contact_data.get('adresse_pays', ''),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                contact_id
            )
            
            success = self.db.execute_update(query, params)
            
            if success:
                self.db.log_action(
                    self.auth.current_user['id'],
                    "Modification contact",
                    "contacts",
                    contact_id
                )
            
            return success
        except Exception as e:
            print(f"Erreur mise à jour contact: {e}")
            return False
    
    def delete_contact(self, contact_id):
        """Supprime un contact"""
        try:
            # Récupérer le nom du contact pour le log
            contact = self.get_contact(contact_id)
            contact_name = f"{contact['prenom']} {contact['nom']}" if contact else str(contact_id)
            
            success = self.db.execute_delete("DELETE FROM contacts WHERE id = ?", (contact_id,))
            
            if success:
                self.db.log_action(
                    self.auth.current_user['id'],
                    "Suppression contact",
                    "contacts",
                    contact_id,
                    contact_name
                )
            
            return success
        except Exception as e:
            print(f"Erreur suppression contact: {e}")
            return False
    
    def get_contact(self, contact_id):
        """Récupère un contact par son ID"""
        query = "SELECT * FROM contacts WHERE id = ?"
        result = self.db.execute_query(query, (contact_id,))
        
        if result and len(result) > 0:
            contact = dict(result[0])
            
            # Ajouter les coordonnées
            contact['coordonnees'] = self.get_coordonnees(contact_id)
            
            # Ajouter les réseaux sociaux
            contact['reseaux_sociaux'] = self.get_reseaux_sociaux(contact_id)
            
            # Ajouter les tags
            contact['tags'] = self.get_contact_tags(contact_id)
            
            return contact
        
        return None
    
    def search_contacts(self, filters=None):
        """Recherche des contacts avec filtres"""
        query = "SELECT * FROM contacts WHERE 1=1"
        params = []
        
        if filters:
            if filters.get('search_text'):
                query += """ AND (
                    nom LIKE ? OR prenom LIKE ? OR societe LIKE ? OR 
                    adresse_ville LIKE ? OR poste LIKE ?
                )"""
                search_term = f"%{filters['search_text']}%"
                params.extend([search_term] * 5)
            
            if filters.get('categorie'):
                query += " AND categorie = ?"
                params.append(filters['categorie'])
            
            if filters.get('ville'):
                query += " AND adresse_ville = ?"
                params.append(filters['ville'])
            
            if filters.get('societe'):
                query += " AND societe = ?"
                params.append(filters['societe'])
        
        query += " ORDER BY nom, prenom"
        
        return self.db.execute_query(query, params if params else None)
    
    def get_all_contacts(self, limit=None, offset=None):
        """Récupère tous les contacts avec pagination optionnelle"""
        query = "SELECT * FROM contacts ORDER BY nom, prenom"
        
        if limit:
            query += f" LIMIT {limit}"
            if offset:
                query += f" OFFSET {offset}"
        
        return self.db.execute_query(query)
    
    def add_coordonnee(self, contact_id, type_coord, valeur, principal=0):
        """Ajoute une coordonnée (téléphone, email) à un contact"""
        query = """
            INSERT INTO coordonnees (contact_id, type_coord, valeur, principal)
            VALUES (?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (contact_id, type_coord, valeur, principal))
    
    def get_coordonnees(self, contact_id):
        """Récupère toutes les coordonnées d'un contact"""
        query = "SELECT * FROM coordonnees WHERE contact_id = ? ORDER BY principal DESC, type_coord"
        return self.db.execute_query(query, (contact_id,))
    
    def delete_coordonnees(self, contact_id):
        """Supprime toutes les coordonnées d'un contact"""
        return self.db.execute_delete("DELETE FROM coordonnees WHERE contact_id = ?", (contact_id,))
    
    def delete_coordonnee(self, coordonnee_id):
        """Supprime une coordonnée"""
        return self.db.execute_delete("DELETE FROM coordonnees WHERE id = ?", (coordonnee_id,))
    
    def add_reseau_social(self, contact_id, plateforme, url):
        """Ajoute un réseau social à un contact"""
        query = """
            INSERT INTO reseaux_sociaux (contact_id, plateforme, url)
            VALUES (?, ?, ?)
        """
        return self.db.execute_insert(query, (contact_id, plateforme, url))
    
    def get_reseaux_sociaux(self, contact_id):
        """Récupère tous les réseaux sociaux d'un contact"""
        query = "SELECT * FROM reseaux_sociaux WHERE contact_id = ?"
        return self.db.execute_query(query, (contact_id,))
    
    def delete_reseaux_sociaux(self, contact_id):
        """Supprime tous les réseaux sociaux d'un contact"""
        return self.db.execute_delete("DELETE FROM reseaux_sociaux WHERE contact_id = ?", (contact_id,))
    
    def delete_reseau_social(self, reseau_id):
        """Supprime un réseau social"""
        return self.db.execute_delete("DELETE FROM reseaux_sociaux WHERE id = ?", (reseau_id,))
    
    def get_contact_tags(self, contact_id):
        """Récupère tous les tags d'un contact"""
        query = """
            SELECT t.id, t.nom_tag
            FROM tags t
            JOIN contact_tags ct ON t.id = ct.tag_id
            WHERE ct.contact_id = ?
        """
        return self.db.execute_query(query, (contact_id,))
    
    def get_categories(self):
        """Récupère toutes les catégories distinctes"""
        query = "SELECT DISTINCT categorie FROM contacts WHERE categorie IS NOT NULL AND categorie != '' ORDER BY categorie"
        result = self.db.execute_query(query)
        return [row['categorie'] for row in result] if result else []
    
    def get_villes(self):
        """Récupère toutes les villes distinctes"""
        query = "SELECT DISTINCT adresse_ville FROM contacts WHERE adresse_ville IS NOT NULL AND adresse_ville != '' ORDER BY adresse_ville"
        result = self.db.execute_query(query)
        return [row['adresse_ville'] for row in result] if result else []
    
    def get_societes(self):
        """Récupère toutes les sociétés distinctes"""
        query = "SELECT DISTINCT societe FROM contacts WHERE societe IS NOT NULL AND societe != '' ORDER BY societe"
        result = self.db.execute_query(query)
        return [row['societe'] for row in result] if result else []
    
    def add_note(self, contact_id, contenu):
        """Ajoute une note à un contact (stockée dans la table contact avec le champ notes)"""
        query = "UPDATE contacts SET notes = ? WHERE id = ?"
        return self.db.execute_update(query, (contenu, contact_id))
    
    def get_notes(self, contact_id):
        """Récupère les notes d'un contact"""
        query = "SELECT notes as contenu, date_modification as date_creation FROM contacts WHERE id = ?"
        result = self.db.execute_query(query, (contact_id,))
        if result and result[0]['contenu']:
            return [result[0]]
        return []
    
    def get_interactions(self, contact_id):
        """Récupère toutes les interactions d'un contact"""
        query = "SELECT * FROM interactions WHERE contact_id = ? ORDER BY date_heure DESC"
        return self.db.execute_query(query, (contact_id,))
