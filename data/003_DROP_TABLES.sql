-- Désactiver temporairement les contraintes pour éviter les erreurs de dépendance
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS tache_contacts;
DROP TABLE IF EXISTS taches;
DROP TABLE IF EXISTS contact_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS relations;
DROP TABLE IF EXISTS rappels;
DROP TABLE IF EXISTS pieces_jointes;
DROP TABLE IF EXISTS interactions;
DROP TABLE IF EXISTS reseaux_sociaux;
DROP TABLE IF EXISTS coordonnees;
DROP TABLE IF EXISTS contacts;
DROP TABLE IF EXISTS projets;
DROP TABLE IF EXISTS users;

-- Réactiver les contraintes
PRAGMA foreign_keys = ON;