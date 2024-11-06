-- Table Logement
CREATE TABLE Logement (
    id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
    adresse TEXT NOT NULL,
    telephone TEXT,
    adresse_ip TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Piece
CREATE TABLE Piece (
    id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
    id_logement INTEGER NOT NULL,
    nom_piece TEXT NOT NULL,
    coord_x INTEGER,
    coord_y INTEGER,
    coord_z INTEGER,
    FOREIGN KEY (id_logement) REFERENCES Logement(id_logement) ON DELETE CASCADE
);

-- Table Type_CapteurActionneur
CREATE TABLE Type_CapteurActionneur (
    id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    type_nom TEXT NOT NULL UNIQUE,
    unite_mesure TEXT,
    plage_precision TEXT
);

-- Table CapteurActionneur
CREATE TABLE CapteurActionneur (
    id_capteur_actionneur INTEGER PRIMARY KEY AUTOINCREMENT,
    id_type INTEGER NOT NULL,
    id_piece INTEGER NOT NULL,
    reference TEXT,
    port_communication TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_type) REFERENCES Type_CapteurActionneur(id_type) ON DELETE SET NULL,
    FOREIGN KEY (id_piece) REFERENCES Piece(id_piece) ON DELETE CASCADE
);

-- Table Mesure
CREATE TABLE Mesure (
    id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
    id_capteur_actionneur INTEGER NOT NULL,
    valeur REAL NOT NULL,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_capteur_actionneur) REFERENCES CapteurActionneur(id_capteur_actionneur) ON DELETE CASCADE
);

-- Table Facture
CREATE TABLE Facture (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    id_logement INTEGER NOT NULL,
    type_facture TEXT NOT NULL,
    date_facture DATE NOT NULL,
    montant REAL NOT NULL,
    valeur_consommation REAL,
    FOREIGN KEY (id_logement) REFERENCES Logement(id_logement) ON DELETE CASCADE
);
