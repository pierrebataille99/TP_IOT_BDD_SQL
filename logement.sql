
-- //////////////////////////////////////////////////////// TP IOT Bases de donnees Pierre BATAILLE ///////////////////////////////////

---------------------------------------------------------- Question 2 ---------------------------------------------------------------
-- On ecrase les donnees precedentes si elles existent
DROP TABLE IF EXISTS Mesure;
DROP TABLE IF EXISTS Facture;
DROP TABLE IF EXISTS Capteur_Actionneur;
DROP TABLE IF EXISTS Type_Capteur_Actionneur;
DROP TABLE IF EXISTS Piece;
DROP TABLE IF EXISTS Logement;




---------------------------------------------------------- Question 3 ---------------------------------------------------------------
-- Creation de toutes les Tables

-- Table Logement (la principale)
CREATE TABLE Logement (
    LOGEMENT_ID TEXT PRIMARY KEY,
    numero_telephone TEXT,
    adresse_ip TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP      -- demande dans le TP
);



-- Table Piece (appartient à Logement)
CREATE TABLE Piece (
    PIECE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    coordonnee_x INTEGER,
    coordonnee_y INTEGER,
    coordonnee_z INTEGER,
    LOGEMENT_ID TEXT,
    FOREIGN KEY (LOGEMENT_ID) REFERENCES Logement(LOGEMENT_ID)
);


-- Table Type_Capteur_Actionneur
CREATE TABLE Type_Capteur_Actionneur (
    TYPE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    unite_mesure TEXT,
    plage_precision TEXT
);


-- Table Capteur_Actionneur
CREATE TABLE Capteur_Actionneur (
    CAPTEUR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TYPE_ID INTEGER,
    reference_commerciale TEXT,
    PIECE_ID INTEGER,
    --port_communication TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (TYPE_ID) REFERENCES Type_Capteur_Actionneur(TYPE_ID),
    FOREIGN KEY (PIECE_ID) REFERENCES Piece(PIECE_ID)
);


-- Table Mesure associee aux capteurs
CREATE TABLE Mesure (
    MESURE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CAPTEUR_ID INTEGER,
    valeur FLOAT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CAPTEUR_ID) REFERENCES Capteur_Actionneur(CAPTEUR_ID)
);


-- Table Facture (par Logement)
CREATE TABLE Facture (
    FACTURE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    LOGEMENT_ID TEXT,
    type_facture TEXT,      -- electricite, eau...
    date_facture DATE,
    montant FLOAT,
    valeur_consomme FLOAT,
    FOREIGN KEY (LOGEMENT_ID) REFERENCES Logement(LOGEMENT_ID)
);






-- ---------------------------------------------------------- Question 4 ---------------------------------------------------------------
-- -- Creation d'un logement avec 4 pieces

-- -- Inserer un logement
-- INSERT INTO Logement (LOGEMENT_ID, numero_telephone, adresse_ip) VALUES 
-- ('LOG001', '0123456789', '192.168.0.1');

-- -- pieces pour le logement
-- INSERT INTO Piece (PIECE_ID, nom, coordonnee_x, coordonnee_y, coordonnee_z, LOGEMENT_ID) VALUES 
-- (1,'Chambre', 0, 1, 0, 'LOG001'),          --piece_ID=1 car autoincrément
-- (2,'WC', 0, 0, 1, 'LOG001'),                  --piece_ID=2
-- (3,'Cuisine', 1, 0, 0, 'LOG001'),            --piece_ID=3
-- (4, 'Salle de Bain', 0, 0, 0, 'LOG001');          --piece_ID=4





-- ---------------------------------------------------------- Question 5 ---------------------------------------------------------------
-- -- Insertion de types de capteurs/actionneurs

-- INSERT INTO Type_Capteur_Actionneur (nom, unite_mesure, plage_precision) VALUES 
-- ('Temperature', '°C', '-10 à 100'),
-- ('Luminosite', 'Lumens', '0 à 10000'),
-- ('Conso elec', 'kWh', '0 à 100'),
-- ('Conso eau', 'L', '0 à 500');





-- ---------------------------------------------------------- Question 6 ---------------------------------------------------------------
-- -- Insertion de capteurs/actionneurs 

-- -- Capteur de temperature pour la Chambre
-- INSERT INTO Capteur_Actionneur (TYPE_ID, reference_commerciale, PIECE_ID) VALUES 
-- (1, 'Capteur Temperature  ', 1);


-- -- Capteur de lumiere pour la Chambre
-- INSERT INTO Capteur_Actionneur (TYPE_ID, reference_commerciale, PIECE_ID) VALUES 
-- (2, 'Capteur Lumière ', 1);


-- -- Capteur de lumière pour les WC
-- INSERT INTO Capteur_Actionneur (TYPE_ID, reference_commerciale, PIECE_ID) VALUES 
-- (2, 'Capteur Lumière ', 2);

-- -- Capteur de consommation electrique pour la Cuisine
-- INSERT INTO Capteur_Actionneur (TYPE_ID, reference_commerciale, PIECE_ID) VALUES 
-- (3, 'Compteur Electrique', 3);


-- -- Capteur de consommation electrique pour la salle de bain
-- INSERT INTO Capteur_Actionneur (TYPE_ID, reference_commerciale, PIECE_ID) VALUES 
-- (4, 'Compteur Eau', 4);



-- ---------------------------------------------------------- Question 7 ---------------------------------------------------------------
-- -- Insertion dune mesure pour chaque capteur/actionneur


-- INSERT INTO Mesure (CAPTEUR_ID, valeur) VALUES 
-- (1, 22.5),
-- (2, 700),
-- (3, 500),
-- (4, 1.2),
-- (5, 30);






-- ---------------------------------------------------------- Question 8 ---------------------------------------------------------------
-- -- Insertion de factures pour le logement

-- -- Facture d'electricite pour le logement 1
-- INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme) VALUES 
-- ('LOG001', 'elec', '2024-01-15', 75.00, 300);

-- -- Facture d'eau pour le logement 1
-- INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme) VALUES 
-- ('LOG001', 'Eau', '2024-01-30', 40.00, 15);

-- -- Facture de dechets pour le logement 1
-- INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme) VALUES 
-- ('LOG001', 'Dechets', '2024-02-01', 20.00, 5);

-- -- Facture supplementaire d'electricite pour le logement 1
-- INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme) VALUES 
-- ('LOG001', 'elec', '2024-02-15', 80.00, 320);
