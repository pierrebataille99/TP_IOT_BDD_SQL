import sqlite3

# Fonction pour supprimer les données des tables Mesure et Facture
def supprimer_donnees_et_reinitialiser_ids():
    conn = sqlite3.connect('bdd_essai1.db')
    c = conn.cursor()

    # Suppression des données dans les tables
    tables = ['Mesure', 'Facture']
    for table in tables:
        c.execute(f"DELETE FROM {table};")
        # Réinitialiser l'AUTOINCREMENT
        c.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")
    
    # Confirmer la suppression et la réinitialisation
    conn.commit()
    conn.close()
    print("Données supprimées et IDs réinitialisés avec succès.")

# Exécution de la fonction
supprimer_donnees_et_reinitialiser_ids()
