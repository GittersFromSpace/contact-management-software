INSERT INTO users (username, password_hash, role, nom, prenom, email) VALUES 
('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'Administrateur', 'Dupont', 'Jean', 'j.dupont@entreprise.fr'),
('m.martin', 'd5c0b8b2c3e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2', 'Utilisateur', 'Martin', 'Marie', 'm.martin@entreprise.fr');

INSERT INTO projets (nom, description, objectif, date_debut, date_fin_previsionnelle) VALUES 
('Refonte Site Web', 'Mise à jour du design et du backend', 'Améliorer le SEO', '2024-01-15', '2024-06-30'),
('Campagne Marketing Q1', 'Publicité sur les réseaux sociaux', 'Acquérir 100 clients', '2024-02-01', '2024-03-15');

INSERT INTO contacts (civilite, nom, prenom, societe, poste, categorie, adresse_ville, adresse_pays, notes) VALUES 
('M.', 'Durand', 'Thomas', 'TechCorp', 'Directeur Technique', 'Client', 'Paris', 'France', 'Client important dans le secteur technologique'),
('Mme', 'Lefebvre', 'Julie', 'Design Studio', 'Graphiste', 'Partenaire', 'Lyon', 'France', 'Partenaire pour les projets de design'),
('M.', 'Smith', 'John', 'Global Inc', 'Acheteur', 'Prospect', 'Londres', 'UK', 'Prospect potentiel pour services IT');

INSERT INTO coordonnees (contact_id, type_coord, valeur, principal) VALUES 
(1, 'Email Pro', 't.durand@techcorp.com', 1),
(1, 'Mobile', '0601020304', 0),
(2, 'Email Pro', 'julie@designstudio.fr', 1);

INSERT INTO reseaux_sociaux (contact_id, plateforme, url) VALUES 
(1, 'LinkedIn', 'https://linkedin.com/in/tdurand'),
(2, 'Instagram', 'https://instagram.com/julesdesign');

INSERT INTO tags (nom_tag) VALUES 
('VIP'), 
('Secteur Tech'), 
('Relance à faire');

INSERT INTO contact_tags (contact_id, tag_id) VALUES 
(1, 1),
(1, 2),
(3, 3);

INSERT INTO interactions (contact_id, type_interaction, date_heure, description, statut) VALUES 
(1, 'Appel Sortant', '2024-01-20 14:30:00', 'Premier contact pour projet refonte', 'Terminé'),
(3, 'Email', '2024-01-21 09:15:00', 'Envoi de la plaquette commerciale', 'En attente');

INSERT INTO pieces_jointes (contact_id, interaction_id, chemin_fichier, description) VALUES 
(3, 2, '/documents/devis_global_inc.pdf', 'Devis envoyé par mail');

INSERT INTO rappels (contact_id, type_rappel, titre, date_heure, priorite) VALUES 
(1, 'Rendez-vous', 'Déjeuner d''affaires', '2024-02-10 12:30:00', 'Haute'),
(3, 'Relance', 'Relancer John pour le devis', '2024-01-28 10:00:00', 'Moyenne');

INSERT INTO relations (contact_source_id, contact_cible_id, type_relation) VALUES 
(1, 2, 'Prestataire');

INSERT INTO taches (titre, description, priorite, statut, projet_id) VALUES 
('Maquette accueil', 'Valider le design de la page home', 'Haute', 'En cours', 1),
('Achat Ads', 'Lancer les annonces Facebook', 'Moyenne', 'A faire', 2);

INSERT INTO tache_contacts (tache_id, contact_id) VALUES 
(1, 2);

INSERT INTO logs (user_id, action, table_cible, cible_id, details) VALUES 
(1, 'CREATE', 'contacts', 1, 'Création du contact Thomas Durand par l''administrateur');