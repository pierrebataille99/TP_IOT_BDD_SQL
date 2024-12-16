# ############################################################# Code de Pierre BATAILLE #################################################
# # TP1 IOT

import sqlite3
import random
from datetime import datetime, timedelta



def recuperer_capteurs(c):
    """
    Récupère tous les capteurs existants dans la base de données.
    Retourne un dictionnaire où chaque capteur est associé à sa plage de valeurs.
    """
    c.execute("SELECT CAPTEUR_ID, TYPE_ID FROM Capteur_Actionneur")
    capteurs = c.fetchall()

    # Plages de valeurs associées à chaque TYPE_ID
    plages_valeurs = {
        1: (10, 30),       # Température : plage 10 à 30 °C
        2: (30, 60),       # Consommation électrique : plage 30 à 60 KW
        3: (5000, 10000),  # Luminosité : plage 5000 à 10000 lumens
        4: (200, 500)      # Niveau d'eau : plage 200 à 500 L
    }

    capteur_plages = {}
    for capteur in capteurs:
        capteur_id, type_id = capteur
        if type_id in plages_valeurs:
            capteur_plages[capteur_id] = plages_valeurs[type_id]

    return capteur_plages







def inserer_mesures(conn, c):
    """
    Insère des mesures pour chaque capteur existant dans la base de données.
    """
    capteur_plages = recuperer_capteurs(c)
    start_date = datetime(2023, 1, 1)  # Date de début
    end_date = datetime(2023, 12, 31)  # Date de fin

    # Parcours de chaque capteur pour générer des mesures
    for capteur_id, (min_val, max_val) in capteur_plages.items():
        current_date = start_date
        while current_date <= end_date:
            valeur = round(random.uniform(min_val, max_val), 2)  # Génère une valeur aléatoire
            date_insertion = current_date.strftime('%Y-%m-%d %H:%M:%S')  # Formatage de la date
            c.execute("""
                INSERT INTO Mesure (CAPTEUR_ID, valeur, date_insertion) 
                VALUES (?, ?, ?)
            """, (capteur_id, valeur, date_insertion))
            current_date += timedelta(days=random.randint(1, 3))  # Saute entre 1 et 3 jours pour ajouter des variations






def inserer_factures(conn, c, logement_id):
    """
    Insère des factures aléatoires pour un logement donné.
    """
    types_factures = ['Elec', 'Eau', 'Dechets']
    for _ in range(50):  # Ajouter 50 factures
        type_facture = random.choice(types_factures)
        date_facture = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format ISO 8601
        montant = round(random.uniform(20.0, 100.0), 2)
        valeur_consomme = round(random.uniform(10.0, 300.0), 2)
        c.execute("""
            INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme)
            VALUES (?, ?, ?, ?, ?)
        """, (logement_id, type_facture, date_facture, montant, valeur_consomme))






def main():
    """
    Fonction principale pour exécuter toutes les étapes.
    """
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

