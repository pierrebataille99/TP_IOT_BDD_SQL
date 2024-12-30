import sys
from pathlib import Path

# Ajout du chemin contenant le serveur Flask au PATH
serveur_dir = Path(__file__).resolve().parents[1]  # Accéder au dossier parent
sys.path.append(str(serveur_dir))

from serveur_restfull_site_3_7 import calculer_factures_par_mesures  # Import de la fonction

import sqlite3
import random
from datetime import datetime, timedelta

# Chemin absolu vers la base de données
db_path = r"D:\01-Etudes\05-Polytech_EI4\29_IOT\02_TP_Partie_Thibault_HILAIRE\Github\TP_IOT_BDD_SQL\bdd_essai1.db"

# Connexion à la base de données
print(f"Connexion à la base de données : {db_path}")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row  # Permet d'accéder aux résultats par nom de colonne
cursor = conn.cursor()

# Création des tables si elles n'existent pas
cursor.executescript('''
CREATE TABLE IF NOT EXISTS Logement (
    LOGEMENT_ID TEXT PRIMARY KEY,
    numero_telephone TEXT,
    adresse_ip TEXT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Piece (
    PIECE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    coordonnee_x INTEGER,
    coordonnee_y INTEGER,
    coordonnee_z INTEGER,
    LOGEMENT_ID TEXT,
    FOREIGN KEY (LOGEMENT_ID) REFERENCES Logement(LOGEMENT_ID)
);

CREATE TABLE IF NOT EXISTS Type_Capteur_Actionneur (
    TYPE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    unite_mesure TEXT,
    plage_precision TEXT
);

CREATE TABLE IF NOT EXISTS Capteur_Actionneur (
    CAPTEUR_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TYPE_ID INTEGER,
    reference_commerciale TEXT,
    PIECE_ID INTEGER,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (TYPE_ID) REFERENCES Type_Capteur_Actionneur(TYPE_ID),
    FOREIGN KEY (PIECE_ID) REFERENCES Piece(PIECE_ID)
);

CREATE TABLE IF NOT EXISTS Mesure (
    MESURE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CAPTEUR_ID INTEGER,
    valeur FLOAT,
    date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CAPTEUR_ID) REFERENCES Capteur_Actionneur(CAPTEUR_ID)
);

CREATE TABLE IF NOT EXISTS Facture (
    FACTURE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    LOGEMENT_ID TEXT,
    type_facture TEXT,
    date_facture DATE,
    montant FLOAT,
    valeur_consomme FLOAT,
    FOREIGN KEY (LOGEMENT_ID) REFERENCES Logement(LOGEMENT_ID)
);
''')
print("Tables vérifiées ou créées avec succès.")

# Réinitialisation des tables
cursor.executescript('''
DELETE FROM Facture;
DELETE FROM Capteur_Actionneur;
DELETE FROM Piece;
DELETE FROM Type_Capteur_Actionneur;
DELETE FROM Logement;
DELETE FROM Mesure;
DELETE FROM sqlite_sequence WHERE name IN (
    'Facture', 'Capteur_Actionneur', 'Piece', 'Type_Capteur_Actionneur', 'Logement', 'Mesure'
);
''')
conn.commit()
print("Tables réinitialisées avec succès.")

# Insertion dans Logement
logements = [
    ('LOG001', '0123456789', '192.168.0.1', '2024-11-27 10:36:33')
]
cursor.executemany("""
INSERT INTO Logement (LOGEMENT_ID, numero_telephone, adresse_ip, date_insertion)
VALUES (?, ?, ?, ?);
""", logements)
conn.commit()
print("Données insérées dans Logement.")

# Insertion dans Piece
pieces = [
    (1, 'Chambre', 0, 1, 0, 'LOG001'),
    (2, 'WC', 0, 0, 1, 'LOG001'),
    (3, 'Cuisine', 1, 0, 0, 'LOG001'),
    (4, 'Salle de Bain', 0, 0, 0, 'LOG001'),
    (5, 'Garage', 2, 4, 3, 'LOG001'),
    (6, 'Salon', 2, 3, 1, 'LOG001')
]
cursor.executemany("""
INSERT INTO Piece (PIECE_ID, nom, coordonnee_x, coordonnee_y, coordonnee_z, LOGEMENT_ID)
VALUES (?, ?, ?, ?, ?, ?);
""", pieces)
conn.commit()
print("Données insérées dans Piece.")

# Insertion dans Type_Capteur_Actionneur
types_capteurs = [
    (1, 'Compteur elec', 'kWh', '0 à 20'),
    (2, 'Compteur eau', 'L', '0 à 100'),
    (3, 'Compteur Gaz', 'm³', '0 à 0.1'),
    (4, 'Capteur Température', '°C', '0 à 3'),
    (5, 'Capteur Humidité', '%', '0 à 100'),
    (6, 'Compteur Dechets', 'kg', '0 à 10')
]
cursor.executemany("""
INSERT INTO Type_Capteur_Actionneur (TYPE_ID, nom, unite_mesure, plage_precision)
VALUES (?, ?, ?, ?);
""", types_capteurs)
conn.commit()
print("Données insérées dans Type_Capteur_Actionneur.")

# Insertion dans Capteur_Actionneur
capteurs = [
    (1, 1, 'Linki', 1, '2024-11-27 10:36:33'),
    (2, 2, 'Gardena', 2, '2024-11-27 10:36:33'),
    (3, 3, 'Gazpar', 3, '2024-11-27 10:36:33'),
    (4, 6, 'dechet_kilo', 4, '2024-11-27 10:36:33'),
    (5, 4, 'Testo', 4, '2024-12-28 10:36:33')
]
cursor.executemany("""
INSERT INTO Capteur_Actionneur (CAPTEUR_ID, TYPE_ID, reference_commerciale, PIECE_ID, date_insertion)
VALUES (?, ?, ?, ?, ?);
""", capteurs)
conn.commit()
print("Données insérées dans Capteur_Actionneur.")

# Insertion dans Mesure
start_date = datetime(2024, 1, 1)
def generate_random_measures(capteur_id, count=10):
    measures = []
    for _ in range(count):
        valeur = round(random.uniform(10.0, 100.0), 2)  # Valeur aléatoire
        date_insertion = start_date + timedelta(days=random.randint(0, 365))
        measures.append((capteur_id, valeur, date_insertion.strftime('%Y-%m-%d %H:%M:%S')))
    return measures

mesures = []
for capteur_id in range(1, 5):
    mesures.extend(generate_random_measures(capteur_id))

cursor.executemany("""
INSERT INTO Mesure (CAPTEUR_ID, valeur, date_insertion)
VALUES (?, ?, ?);
""", mesures)
conn.commit()
print("Données insérées dans Mesure.")

# Calcul des factures dynamiquement
factures_calculées = calculer_factures_par_mesures('LOG001')
print("Factures calculées :", factures_calculées)

# Insertion dans Facture
for type_facture, valeur_consommée in factures_calculées.items():
    cursor.execute("""
        INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, valeur_consomme)
        VALUES (?, ?, ?, ?)
    """, ('LOG001', type_facture, datetime.now().strftime('%Y-%m-%d'), valeur_consommée))
conn.commit()
print("Données insérées dans Facture.")

# Mise à jour des prix par unité
prix_par_unite = {
    'Compteur elec': 0.2516,
    'Compteur eau': 0.00414,
    'Compteur Gaz': 0.956,   # prix m3 gaz
    'Capteur Dechets': 0.05
}

cursor.execute("SELECT FACTURE_ID, type_facture, valeur_consomme FROM Facture")
factures = cursor.fetchall()
for facture in factures:
    facture_id = facture["FACTURE_ID"]
    type_facture = facture["type_facture"]
    valeur_consomme = facture["valeur_consomme"]
    prix = valeur_consomme * prix_par_unite.get(type_facture, 0)
    cursor.execute("""
        UPDATE Facture
        SET montant = ?
        WHERE FACTURE_ID = ?
    """, (round(prix, 2), facture_id))
conn.commit()
print("Prix mis à jour pour chaque facture.")

# Vérification des données insérées
cursor.execute("SELECT * FROM Facture")
factures = cursor.fetchall()
print("Factures insérées :", factures)

# Validation et fermeture
conn.close()
print("Données insérées avec succès.")
