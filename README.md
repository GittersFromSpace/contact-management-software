# contact-management-software# Application de Gestion de Contacts Avancée

Application desktop complète pour la gestion professionnelle de contacts avec suivi des interactions, rappels, tâches et projets.

## 📋 Fonctionnalités principales

### Module de Gestion des Contacts
- ✅ Ajout, modification, suppression de contacts
- ✅ Informations complètes : civilité, nom, prénom, société, poste, catégorie
- ✅ Coordonnées multiples (téléphones, emails)
- ✅ Adresse postale complète
- ✅ Réseaux sociaux (LinkedIn, Twitter, etc.)
- ✅ Notes libres
- ✅ Recherche avancée multicritères
- ✅ Filtres par catégorie, ville, société

### Module Interactions et Historique
- ✅ Enregistrement des interactions avec les contacts
- ✅ Types d'interactions personnalisables
- ✅ Historique chronologique
- ✅ Pièces jointes
- ✅ Recherche et filtrage

### Module Rappels et Anniversaires
- ✅ Création de rappels liés aux contacts
- ✅ Gestion des priorités
- ✅ Tableau de bord des rappels du jour
- ✅ Notifications et suivi

### Module Tags et Relations
- ✅ Système de tags personnalisés
- ✅ Assignation multiple de tags
- ✅ Relations entre contacts
- ✅ Filtrage par tags combinés

### Module Tâches et Projets
- ✅ Création de tâches liées aux contacts (obligatoire)
- ✅ Gestion des priorités et statuts
- ✅ Organisation en projets
- ✅ Suivi de l'avancement
- ✅ Échéances et rappels

### Module Import/Export
- ✅ Import CSV avec mapping personnalisé
- ✅ Export CSV
- ✅ Export vCard (.vcf)
- ✅ Détection de doublons
- ✅ Fusion de contacts

### Module Statistiques et Rapports
- ✅ Statistiques globales
- ✅ Répartition par catégorie, ville, pays, tags
- ✅ Contacts les plus actifs
- ✅ Évolution des ajouts dans le temps
- ✅ Génération de graphiques (Matplotlib)
- ✅ Export des rapports en CSV

### Module Administration et Sécurité
- ✅ Authentification par mot de passe (hachage SHA-256)
- ✅ Multi-profils (propriétaire / consultant)
- ✅ Sauvegarde de la base de données
- ✅ Journal des modifications (logs)

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8 ou supérieur
- tkinter (inclus avec Python sur la plupart des systèmes)
- SQLite3 (inclus avec Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Initialisation de la base de données

La base de données SQLite sera créée automatiquement au premier lancement. Les tables seront initialisées à partir du script SQL `data/001_CREATE_TABLES.sql`.

### Lancement de l'application

```bash
python main.py
```

Ou :

```bash
python3 main.py
```

### Connexion par défaut

```
Nom d'utilisateur : admin
Mot de passe : admin
```

**⚠️ Important :** Changez le mot de passe par défaut après la première connexion !

## 📁 Structure du projet

```
contact-management-software/
├── main.py                          # Point d'entrée principal
├── requirements.txt                 # Dépendances Python
├── README.md                        # Documentation
├── contacts.db                      # Base de données SQLite (créée au runtime)
│
├── data/                            # Scripts SQL
│   ├── 001_CREATE_TABLES.sql       # Création des tables
│   ├── 002_INSERT_DATA.sql         # Données de test (optionnel)
│   └── 003_DROP_TABLES.sql         # Suppression des tables
│
├── src/                             # Code source
│   ├── main_app.py                  # Application principale
│   │
│   ├── utils/                       # Utilitaires
│   │   ├── database_manager.py      # Gestionnaire de base de données
│   │   └── auth_manager.py          # Authentification
│   │
│   └── modules/                     # Modules métier
│       ├── contact_manager.py       # Gestion des contacts
│       ├── contact_ui.py            # Interface graphique contacts
│       ├── interaction_manager.py   # Interactions et rappels
│       ├── tag_relation_manager.py  # Tags et relations
│       ├── task_manager.py          # Tâches et projets
│       ├── import_export_manager.py # Import/Export
│       └── statistics_manager.py    # Statistiques
│
├── exports/                         # Dossier pour les exports
└── uploads/                         # Dossier pour les fichiers uploadés
```

## 🗄️ Base de données

La base de données SQLite contient les tables suivantes :

- **users** : Utilisateurs de l'application
- **contacts** : Informations principales des contacts
- **coordonnees** : Téléphones et emails multiples
- **reseaux_sociaux** : Profils sur les réseaux sociaux
- **interactions** : Historique des échanges
- **pieces_jointes** : Fichiers attachés
- **rappels** : Rappels et anniversaires
- **relations** : Liens entre contacts
- **tags** : Étiquettes personnalisées
- **contact_tags** : Association contacts-tags
- **taches** : Tâches liées aux contacts
- **tache_contacts** : Association tâches-contacts
- **projets** : Projets regroupant des tâches
- **logs** : Journal des modifications

## 🎯 Utilisation

### Gestion des contacts

1. **Ajouter un contact** : Cliquez sur "➕ Nouveau contact" dans l'onglet Contacts
2. **Rechercher** : Utilisez la barre de recherche et les filtres (catégorie, ville)
3. **Modifier** : Sélectionnez un contact et cliquez sur "✏ Modifier"
4. **Voir les détails** : Double-cliquez sur un contact ou cliquez sur "👁 Voir détails"

### Interactions

1. Accédez à l'onglet "💬 Interactions"
2. Cliquez sur "➕ Nouvelle interaction"
3. Sélectionnez le contact, le type d'interaction et ajoutez une description

### Rappels

1. Onglet "🔔 Rappels"
2. Créez des rappels avec date/heure, priorité et répétition
3. Le tableau de bord affiche les rappels du jour

### Tâches et Projets

1. Onglet "✓ Tâches"
2. Créez des tâches en associant au moins un contact (obligatoire)
3. Organisez les tâches en projets dans l'onglet "📁 Projets"
4. Suivez l'avancement avec les statistiques de projet

### Import/Export

**Import CSV :**
- Menu "Import/Export" > "Importer CSV"
- Mappez les colonnes du CSV avec les champs de la base
- Les doublons sont détectés automatiquement

**Export :**
- CSV : Menu "Import/Export" > "Exporter CSV"
- vCard : Menu "Import/Export" > "Exporter vCard"

### Statistiques

1. Menu "Statistiques" > "Voir les statistiques" pour un aperçu rapide
2. "Générer des graphiques" pour créer des visualisations (camemberts, barres, courbes)
3. "Exporter statistiques CSV" pour analyse externe

## 🔒 Sécurité

- Mots de passe hachés avec SHA-256
- Deux rôles : **propriétaire** (tous droits) et **consultant** (lecture seule)
- Journal complet des modifications
- Sauvegarde de la base de données

## 🛠️ Développement

### Ajouter un module

1. Créez un nouveau fichier dans `src/modules/`
2. Importez-le dans `src/main_app.py`
3. Ajoutez un onglet dans l'interface si nécessaire

### Structure d'un module métier

```python
class MonManager:
    def __init__(self, db_manager, auth_manager):
        self.db = db_manager
        self.auth = auth_manager
    
    def create_item(self, data):
        pass
```