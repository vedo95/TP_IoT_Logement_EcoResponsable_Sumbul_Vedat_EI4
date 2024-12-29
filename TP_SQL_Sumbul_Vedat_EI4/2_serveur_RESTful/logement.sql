-- Logement.sql : Script SQL pour le TP Eco-Responsable
-- Ce fichier contient les commandes SQL pour détruire, créer et préparer les tables de la base.

-- =======================================================
-- Question 2 : Détruire toutes les tables existantes
-- =======================================================
DROP TABLE IF EXISTS Mesures;
DROP TABLE IF EXISTS Capteurs_Actionneurs;
DROP TABLE IF EXISTS Type_Capt_Actionneur;
DROP TABLE IF EXISTS Pieces;
DROP TABLE IF EXISTS Factures;
DROP TABLE IF EXISTS Logements;

-- =======================================================
-- Question 3 : Créer toutes les tables de la base
-- =======================================================

-- Table des logements
-- Contient les informations des logements
CREATE TABLE Logements (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT NOT NULL,
    numero_telephone TEXT NOT NULL,
    adresse_ip TEXT NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des pièces
-- Contient les informations des pièces associées à un logement
CREATE TABLE Pieces (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_piece TEXT NOT NULL,
    x_coord INTEGER NOT NULL,
    y_coord INTEGER NOT NULL,
    z_coord INTEGER NOT NULL,
    id_logement INTEGER NOT NULL,
    FOREIGN KEY (id_logement) REFERENCES Logements (id_logement)
);

-- Table des capteurs/actionneurs
-- Contient les informations des capteurs/actionneurs associés à une pièce
CREATE TABLE Capteurs_Actionneurs (
    id_capt_act INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    reference_commerciale TEXT NOT NULL,
    port_communication TEXT NOT NULL,
    id_piece INTEGER NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_piece) REFERENCES Pieces (id_piece)
);

-- Table des types de capteurs/actionneurs
-- Contient les types de capteurs/actionneurs avec leurs propriétés communes
CREATE TABLE Type_Capt_Actionneur (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_type TEXT NOT NULL,
    unite_mesure TEXT NOT NULL,
    plage_precision TEXT NOT NULL
);

-- Table des mesures
-- Contient les mesures enregistrées par les capteurs/actionneurs
CREATE TABLE Mesures (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    id_capt_act INTEGER NOT NULL,
    valeur REAL NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_capt_act) REFERENCES Capteurs_Actionneurs (id_capt_act)
);

-- Table des factures
-- Contient les factures associées aux logements
CREATE TABLE Factures (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    id_logement INTEGER NOT NULL,
    type TEXT NOT NULL,
    date_facture DATE NOT NULL,
    montant REAL NOT NULL,
    consommation REAL NOT NULL,
    FOREIGN KEY (id_logement) REFERENCES Logements (id_logement)
);

-- Fin du script
