import sqlite3
import random
from datetime import datetime, timedelta


# Génération de mesures aléatoires pour les capteurs
def inserer_mesures(conn, c):
    capteur_ids = {
        1: (-10, 100),  # Température : plage -10 à 100
        2: (0, 100),    # Consommation électrique : plage 0 à 100
        3: (0, 10000),  # Luminosité : plage 0 à 10000
        4: (0, 500)     # Niveau d'eau : plage 0 à 500
    }
    for capteur_id, (min_val, max_val) in capteur_ids.items():
        for _ in range(5):  # Ajouter 5 mesures pour chaque capteur
            valeur = round(random.uniform(min_val, max_val), 2)
            date_insertion = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
            c.execute("""
                INSERT INTO Mesure (CAPTEUR_ID, valeur, date_insertion) 
                VALUES (?, ?, ?)
            """, (capteur_id, valeur, date_insertion))









# Génération de factures aléatoires pour un logement donné
def inserer_factures(conn, c, logement_id):
    types_factures = ['elec', 'Eau', 'Dechets']
    for _ in range(5):  # Ajouter 5 factures
        type_facture = random.choice(types_factures)
        date_facture = datetime.now() 
        montant = round(random.uniform(20.0, 100.0), 2)
        valeur_consomme = round(random.uniform(10.0, 300.0), 2)
        c.execute("""
            INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme)
            VALUES (?, ?, ?, ?, ?)
        """, (logement_id, type_facture, date_facture, montant, valeur_consomme))








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
