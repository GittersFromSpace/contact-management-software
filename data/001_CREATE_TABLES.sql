PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT,
    nom TEXT,
    prenom TEXT,
    email TEXT,
    actif INTEGER DEFAULT 1, -- 1 pour vrai, 0 pour faux
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    dernier_login DATETIME
);

CREATE TABLE IF NOT EXISTS projets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    description TEXT,
    objectif TEXT,
    date_debut DATE,
    date_fin_previsionnelle DATE,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_fin DATE
);

CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    civilite TEXT,
    nom TEXT NOT NULL,
    prenom TEXT,
    societe TEXT,
    poste TEXT,
    categorie TEXT,
    photo_path TEXT,
    date_naissance DATE,
    anniversaire_professionnel DATE,
    site_web TEXT,
    adresse_rue TEXT,
    adresse_code_postal TEXT,
    adresse_ville TEXT,
    adresse_pays TEXT,
    notes TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME
);

CREATE TABLE IF NOT EXISTS coordonnees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER,
    type_coord TEXT,
    valeur TEXT NOT NULL,
    principal INTEGER DEFAULT 0,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reseaux_sociaux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER,
    plateforme TEXT,
    url TEXT,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER,
    type_interaction TEXT,
    date_heure DATETIME,
    description TEXT,
    statut TEXT,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pieces_jointes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER,
    interaction_id INTEGER,
    chemin_fichier TEXT NOT NULL,
    description TEXT,
    date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
    FOREIGN KEY (interaction_id) REFERENCES interactions(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS rappels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER,
    type_rappel TEXT,
    titre TEXT NOT NULL,
    date_heure DATETIME,
    description TEXT,
    priorite TEXT,
    repetition TEXT,
    traite INTEGER DEFAULT 0,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_source_id INTEGER,
    contact_cible_id INTEGER,
    type_relation TEXT,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contact_source_id) REFERENCES contacts(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_cible_id) REFERENCES contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_tag TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS contact_tags (
    contact_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (contact_id, tag_id),
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS taches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT,
    date_echeance DATETIME,
    priorite TEXT,
    statut TEXT,
    projet_id INTEGER,
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modification DATETIME,
    FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS tache_contacts (
    tache_id INTEGER,
    contact_id INTEGER,
    PRIMARY KEY (tache_id, contact_id),
    FOREIGN KEY (tache_id) REFERENCES taches(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_id) REFERENCES contacts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    date_action DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    table_cible TEXT,
    cible_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);