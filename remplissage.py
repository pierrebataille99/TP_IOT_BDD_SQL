############################################################# Code de Pierre BATAILLE #################################################
# TP1 IOT

import sqlite3
import random
from datetime import datetime, timedelta


def inserer_mesures(conn, c):
    capteur_ids = {
        1: (10, 30),       # Température : plage 10 à 30 °C
        2: (30, 60),       # Consommation électrique : plage 30 à 60 KW
        3: (5000, 10000),  # Luminosité : plage 5000 à 10000 lumens
        4: (200, 500),     # Niveau d'eau : plage 200 à 500 L
        5: (10, 30),       # Température : plage 10 à 30 °C
    }
    start_date = datetime(2023, 1, 1)  # Date de début
    end_date = datetime(2023, 12, 31)  # Date de fin

    # Parcours de chaque capteur pour générer des mesures
    for capteur_id, (min_val, max_val) in capteur_ids.items():
        current_date = start_date
        while current_date <= end_date:
            valeur = round(random.uniform(min_val, max_val), 2)  # Génère une valeur aléatoire
            date_insertion = current_date.strftime('%Y-%m-%d %H:%M:%S')  # Formatage de la date
            c.execute("""
                INSERT INTO Mesure (CAPTEUR_ID, valeur, date_insertion) 
                VALUES (?, ?, ?)
            """, (capteur_id, valeur, date_insertion))
            current_date += timedelta(days=random.randint(1, 3))  # Saute entre 1 et 3 jours pour ajouter des variations








# Génération de factures aleat pour le log01
def inserer_factures(conn, c, logement_id):
    types_factures = ['Elec', 'Eau', 'Dechets']
    for _ in range(50):  # Ajouter 5 factures
        type_facture = random.choice(types_factures)
        date_facture = datetime.now() 
        montant = round(random.uniform(20.0, 100.0), 2)
        valeur_consomme = round(random.uniform(10.0, 300.0), 2)
        c.execute("""
            INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme)
            VALUES (?, ?, ?, ?, ?)
        """, (logement_id, type_facture, date_facture, montant, valeur_consomme))







def inserer_capteurs(conn, c, piece_id):
    """
    Insère les 4 types de capteurs (Température, Luminosité, Consommation électrique, Consommation d'eau)
    pour une pièce spécifique identifiée par piece_id.
    """
    capteurs = [
        {"TYPE_ID": 1, "reference_commerciale": "Capteur Température"},
        {"TYPE_ID": 2, "reference_commerciale": "Capteur Luminosité"},
        {"TYPE_ID": 3, "reference_commerciale": "Compteur Électrique"},
        {"TYPE_ID": 4, "reference_commerciale": "Compteur Eau"}
    ]
    
    for capteur in capteurs:
        c.execute("""
            INSERT INTO Capteur_Actionneur (TYPE_ID, reference_commerciale, PIECE_ID)
            VALUES (?, ?, ?)
        """, (capteur["TYPE_ID"], capteur["reference_commerciale"], piece_id))
 






# Fonction principale pour exécuter toutes les étapes
def main():
    # Connexion à la base de données
    conn = sqlite3.connect('bdd_essai1.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Insertion de mesures et de factures
    inserer_mesures(conn, c)
    inserer_factures(conn, c, 'LOG001')  # Exemple avec LOGEMENT_ID existant
    
    # Fermeture de la connexion
    conn.commit()
    conn.close()

# Exécution du programme
if __name__ == '__main__':
    main()
