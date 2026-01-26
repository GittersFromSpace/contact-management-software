"""Module d'import/export et gestion des doublons"""
import csv
import os
from datetime import datetime


class ImportExportManager:
    """Gère l'import et l'export de contacts"""
    
    def __init__(self, db_manager, auth_manager, contact_manager):
        self.db = db_manager
        self.auth = auth_manager
        self.contact_mgr = contact_manager
    
    def import_from_csv(self, file_path, mapping):
        """Importe des contacts depuis un fichier CSV
        
        Args:
            file_path: Chemin du fichier CSV
            mapping: Dictionnaire de correspondance {colonne_csv: champ_db}
        
        Returns:
            Tuple (success, nb_imported, nb_duplicates, errors)
        """
        try:
            imported = 0
            duplicates = 0
            errors = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Créer l'objet contact à partir du mapping
                        contact_data = {}
                        
                        for csv_col, db_field in mapping.items():
                            if csv_col in row and db_field:
                                contact_data[db_field] = row[csv_col]
                        
                        # Vérifier si le contact existe déjà (doublon)
                        if self.is_duplicate(contact_data):
                            duplicates += 1
                            continue
                        
                        # Créer le contact
                        success, contact_id = self.contact_mgr.create_contact(contact_data)
                        
                        if success:
                            imported += 1
                        else:
                            errors.append(f"Ligne {row_num}: Erreur création")
                    
                    except Exception as e:
                        errors.append(f"Ligne {row_num}: {str(e)}")
            
            self.db.log_action(
                self.auth.current_user['id'],
                "Import CSV",
                "contacts",
                None,
                f"Importés: {imported}, Doublons: {duplicates}"
            )
            
            return True, imported, duplicates, errors
        
        except Exception as e:
            return False, 0, 0, [str(e)]
    
    def export_to_csv(self, file_path, contact_ids=None):
        """Exporte des contacts vers un fichier CSV"""
        try:
            # Récupérer les contacts
            if contact_ids:
                contacts = [self.contact_mgr.get_contact(cid) for cid in contact_ids]
                contacts = [c for c in contacts if c]  # Filtrer les None
            else:
                contacts = self.contact_mgr.get_all_contacts()
            
            if not contacts:
                return False, "Aucun contact à exporter"
            
            # Définir les champs à exporter
            fieldnames = [
                'id', 'civilite', 'nom', 'prenom', 'societe', 'poste', 'categorie',
                'date_naissance', 'site_web', 'adresse_rue', 'adresse_code_postal',
                'adresse_ville', 'adresse_pays'
            ]
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for contact in contacts:
                    row = {field: contact.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            self.db.log_action(
                self.auth.current_user['id'],
                "Export CSV",
                "contacts",
                None,
                f"{len(contacts)} contacts exportés"
            )
            
            return True, f"{len(contacts)} contacts exportés avec succès"
        
        except Exception as e:
            return False, str(e)
    
    def export_to_vcard(self, file_path, contact_ids=None):
        """Exporte des contacts au format vCard (.vcf)"""
        try:
            # Récupérer les contacts
            if contact_ids:
                contacts = [self.contact_mgr.get_contact(cid) for cid in contact_ids]
                contacts = [c for c in contacts if c]
            else:
                contacts = self.contact_mgr.get_all_contacts()
            
            if not contacts:
                return False, "Aucun contact à exporter"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                for contact in contacts:
                    # Format vCard 3.0
                    f.write("BEGIN:VCARD\n")
                    f.write("VERSION:3.0\n")
                    
                    # Nom
                    nom = contact.get('nom', '')
                    prenom = contact.get('prenom', '')
                    f.write(f"N:{nom};{prenom};;;\n")
                    f.write(f"FN:{prenom} {nom}\n")
                    
                    # Société et poste
                    if contact.get('societe'):
                        f.write(f"ORG:{contact['societe']}\n")
                    if contact.get('poste'):
                        f.write(f"TITLE:{contact['poste']}\n")
                    
                    # Coordonnées
                    if contact.get('coordonnees'):
                        for coord in contact['coordonnees']:
                            if coord['type_coord'] == 'email':
                                f.write(f"EMAIL:{coord['valeur']}\n")
                            elif coord['type_coord'] in ['mobile', 'fixe', 'telephone']:
                                f.write(f"TEL;TYPE=CELL:{coord['valeur']}\n")
                    
                    # Adresse
                    rue = contact.get('adresse_rue', '')
                    ville = contact.get('adresse_ville', '')
                    cp = contact.get('adresse_code_postal', '')
                    pays = contact.get('adresse_pays', '')
                    
                    if rue or ville:
                        f.write(f"ADR:;;{rue};{ville};;{cp};{pays}\n")
                    
                    # URL
                    if contact.get('site_web'):
                        f.write(f"URL:{contact['site_web']}\n")
                    
                    # Date de naissance
                    if contact.get('date_naissance'):
                        f.write(f"BDAY:{contact['date_naissance']}\n")
                    
                    f.write("END:VCARD\n\n")
            
            self.db.log_action(
                self.auth.current_user['id'],
                "Export vCard",
                "contacts",
                None,
                f"{len(contacts)} contacts exportés"
            )
            
            return True, f"{len(contacts)} contacts exportés avec succès"
        
        except Exception as e:
            return False, str(e)
    
    def is_duplicate(self, contact_data):
        """Vérifie si un contact est un doublon potentiel"""
        nom = contact_data.get('nom', '').strip().lower()
        prenom = contact_data.get('prenom', '').strip().lower()
        
        if not nom:
            return False
        
        # Rechercher des contacts similaires
        query = """
            SELECT id FROM contacts
            WHERE LOWER(nom) = ? AND (
                LOWER(prenom) = ? OR
                ? = ''
            )
            LIMIT 1
        """
        
        result = self.db.execute_query(query, (nom, prenom, prenom))
        
        return result and len(result) > 0
    
    def find_duplicates(self):
        """Trouve tous les doublons potentiels"""
        query = """
            SELECT c1.id as id1, c1.nom as nom1, c1.prenom as prenom1,
                   c2.id as id2, c2.nom as nom2, c2.prenom as prenom2
            FROM contacts c1
            JOIN contacts c2 ON LOWER(c1.nom) = LOWER(c2.nom)
                AND LOWER(c1.prenom) = LOWER(c2.prenom)
                AND c1.id < c2.id
            ORDER BY c1.nom, c1.prenom
        """
        
        return self.db.execute_query(query)
    
    def merge_contacts(self, keep_id, delete_id, field_choices):
        """Fusionne deux contacts
        
        Args:
            keep_id: ID du contact à conserver
            delete_id: ID du contact à supprimer
            field_choices: Dictionnaire {field: source_id} indiquant d'où prendre chaque champ
        """
        try:
            # Récupérer les deux contacts
            contact_keep = self.contact_mgr.get_contact(keep_id)
            contact_delete = self.contact_mgr.get_contact(delete_id)
            
            if not contact_keep or not contact_delete:
                return False, "Contact introuvable"
            
            # Créer le contact fusionné
            merged_data = {}
            
            for field in ['civilite', 'nom', 'prenom', 'societe', 'poste', 'categorie',
                         'date_naissance', 'site_web', 'adresse_rue', 'adresse_code_postal',
                         'adresse_ville', 'adresse_pays']:
                
                source_id = field_choices.get(field, keep_id)
                
                if source_id == keep_id:
                    merged_data[field] = contact_keep.get(field, '')
                else:
                    merged_data[field] = contact_delete.get(field, '')
            
            # Mettre à jour le contact à conserver
            self.contact_mgr.update_contact(keep_id, merged_data)
            
            # Transférer les relations du contact à supprimer vers le contact à conserver
            self.db.execute_update(
                "UPDATE interactions SET contact_id = ? WHERE contact_id = ?",
                (keep_id, delete_id)
            )
            
            self.db.execute_update(
                "UPDATE rappels SET contact_id = ? WHERE contact_id = ?",
                (keep_id, delete_id)
            )
            
            self.db.execute_update(
                "UPDATE tache_contacts SET contact_id = ? WHERE contact_id = ?",
                (keep_id, delete_id)
            )
            
            # Supprimer le contact
            self.contact_mgr.delete_contact(delete_id)
            
            self.db.log_action(
                self.auth.current_user['id'],
                "Fusion contacts",
                "contacts",
                keep_id,
                f"Fusion {delete_id} -> {keep_id}"
            )
            
            return True, "Contacts fusionnés avec succès"
        
        except Exception as e:
            return False, str(e)
