"""Module de statistiques et rapports"""
from datetime import datetime
import os


class StatisticsManager:
    """Gère les statistiques et rapports"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_contacts_by_category(self):
        """Nombre de contacts par catégorie"""
        query = """
            SELECT categorie, COUNT(*) as nombre
            FROM contacts
            WHERE categorie IS NOT NULL AND categorie != ''
            GROUP BY categorie
            ORDER BY nombre DESC
        """
        return self.db.execute_query(query)
    
    def get_contacts_by_tag(self):
        """Nombre de contacts par tag"""
        query = """
            SELECT t.nom_tag, COUNT(ct.contact_id) as nombre
            FROM tags t
            LEFT JOIN contact_tags ct ON t.id = ct.tag_id
            GROUP BY t.id, t.nom_tag
            ORDER BY nombre DESC
        """
        return self.db.execute_query(query)
    
    def get_contacts_by_city(self):
        """Nombre de contacts par ville"""
        query = """
            SELECT adresse_ville as ville, COUNT(*) as nombre
            FROM contacts
            WHERE adresse_ville IS NOT NULL AND adresse_ville != ''
            GROUP BY adresse_ville
            ORDER BY nombre DESC
        """
        return self.db.execute_query(query)
    
    def get_contacts_by_country(self):
        """Nombre de contacts par pays"""
        query = """
            SELECT adresse_pays as pays, COUNT(*) as nombre
            FROM contacts
            WHERE adresse_pays IS NOT NULL AND adresse_pays != ''
            GROUP BY adresse_pays
            ORDER BY nombre DESC
        """
        return self.db.execute_query(query)
    
    def get_contacts_evolution(self, period='month'):
        """Évolution du nombre de contacts dans le temps"""
        if period == 'month':
            date_format = '%Y-%m'
            label = 'Mois'
        else:  # year
            date_format = '%Y'
            label = 'Année'
        
        query = f"""
            SELECT strftime('{date_format}', date_creation) as periode, COUNT(*) as nombre
            FROM contacts
            WHERE date_creation IS NOT NULL
            GROUP BY periode
            ORDER BY periode
        """
        
        result = self.db.execute_query(query)
        return [(r['periode'], r['nombre']) for r in result] if result else []
    
    def get_most_active_contacts(self, limit=10):
        """Contacts avec le plus d'interactions"""
        query = """
            SELECT c.id, c.nom, c.prenom, c.societe, COUNT(i.id) as nb_interactions
            FROM contacts c
            LEFT JOIN interactions i ON c.id = i.contact_id
            GROUP BY c.id, c.nom, c.prenom, c.societe
            HAVING nb_interactions > 0
            ORDER BY nb_interactions DESC
            LIMIT ?
        """
        return self.db.execute_query(query, (limit,))
    
    def get_global_statistics(self):
        """Statistiques globales"""
        stats = {}
        
        # Total contacts
        result = self.db.execute_query("SELECT COUNT(*) as total FROM contacts")
        stats['total_contacts'] = result[0]['total'] if result else 0
        
        # Total interactions
        result = self.db.execute_query("SELECT COUNT(*) as total FROM interactions")
        stats['total_interactions'] = result[0]['total'] if result else 0
        
        # Total rappels actifs
        result = self.db.execute_query("SELECT COUNT(*) as total FROM rappels WHERE traite = 0")
        stats['rappels_actifs'] = result[0]['total'] if result else 0
        
        # Total tâches
        result = self.db.execute_query("SELECT COUNT(*) as total FROM taches")
        stats['total_taches'] = result[0]['total'] if result else 0
        
        # Tâches en cours
        result = self.db.execute_query("SELECT COUNT(*) as total FROM taches WHERE statut = 'En cours'")
        stats['taches_en_cours'] = result[0]['total'] if result else 0
        
        # Total tags
        result = self.db.execute_query("SELECT COUNT(*) as total FROM tags")
        stats['total_tags'] = result[0]['total'] if result else 0
        
        # Total projets
        result = self.db.execute_query("SELECT COUNT(*) as total FROM projets")
        stats['total_projets'] = result[0]['total'] if result else 0
        
        return stats
    
    def export_statistics_to_csv(self, file_path):
        """Exporte les statistiques vers un fichier CSV"""
        import csv
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Statistiques globales
                writer.writerow(["=== STATISTIQUES GLOBALES ==="])
                stats = self.get_global_statistics()
                for key, value in stats.items():
                    writer.writerow([key.replace('_', ' ').title(), value])
                
                writer.writerow([])
                
                # Par catégorie
                writer.writerow(["=== CONTACTS PAR CATÉGORIE ==="])
                writer.writerow(["Catégorie", "Nombre"])
                for row in self.get_contacts_by_category():
                    writer.writerow([row['categorie'], row['nombre']])
                
                writer.writerow([])
                
                # Par ville
                writer.writerow(["=== CONTACTS PAR VILLE ==="])
                writer.writerow(["Ville", "Nombre"])
                for row in self.get_contacts_by_city():
                    writer.writerow([row['ville'], row['nombre']])
                
                writer.writerow([])
                
                # Contacts les plus actifs
                writer.writerow(["=== CONTACTS LES PLUS ACTIFS ==="])
                writer.writerow(["Nom", "Prénom", "Société", "Nb Interactions"])
                for row in self.get_most_active_contacts():
                    writer.writerow([
                        row['nom'], row['prenom'],
                        row['societe'] or '', row['nb_interactions']
                    ])
            
            return True, "Statistiques exportées avec succès"
        
        except Exception as e:
            return False, str(e)
    
    def generate_charts(self, output_dir):
        """Génère des graphiques avec Matplotlib"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')  # Backend non-interactif
            
            os.makedirs(output_dir, exist_ok=True)
            
            # 1. Camembert par catégorie
            data = self.get_contacts_by_category()
            if data:
                labels = [row['categorie'] for row in data]
                sizes = [row['nombre'] for row in data]
                
                plt.figure(figsize=(10, 6))
                plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                plt.title('Répartition des contacts par catégorie')
                plt.axis('equal')
                plt.savefig(os.path.join(output_dir, 'contacts_par_categorie.png'))
                plt.close()
            
            # 2. Barres par ville (top 10)
            data = self.get_contacts_by_city()
            if data:
                top_10 = data[:10]
                villes = [row['ville'] for row in top_10]
                nombres = [row['nombre'] for row in top_10]
                
                plt.figure(figsize=(12, 6))
                plt.bar(villes, nombres)
                plt.xlabel('Ville')
                plt.ylabel('Nombre de contacts')
                plt.title('Top 10 des villes')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'contacts_par_ville.png'))
                plt.close()
            
            # 3. Évolution dans le temps
            data = self.get_contacts_evolution('month')
            if data and len(data) > 1:
                periodes = [d[0] for d in data]
                nombres = [d[1] for d in data]
                
                plt.figure(figsize=(12, 6))
                plt.plot(periodes, nombres, marker='o')
                plt.xlabel('Période')
                plt.ylabel('Nombre de nouveaux contacts')
                plt.title('Évolution des ajouts de contacts par mois')
                plt.xticks(rotation=45, ha='right')
                plt.grid(True)
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'evolution_contacts.png'))
                plt.close()
            
            # 4. Contacts les plus actifs
            data = self.get_most_active_contacts(10)
            if data:
                noms = [f"{row['prenom']} {row['nom']}" for row in data]
                interactions = [row['nb_interactions'] for row in data]
                
                plt.figure(figsize=(12, 6))
                plt.barh(noms, interactions)
                plt.xlabel('Nombre d\'interactions')
                plt.title('Top 10 des contacts les plus actifs')
                plt.tight_layout()
                plt.savefig(os.path.join(output_dir, 'contacts_actifs.png'))
                plt.close()
            
            return True, "Graphiques générés avec succès"
        
        except ImportError:
            return False, "Matplotlib n'est pas installé"
        except Exception as e:
            return False, str(e)
