import sqlite3
import os

def supprimer_donnees_toutes_tables():
    try:
        # Déterminer le chemin absolu vers le fichier de la base de données
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire contenant ce script
        db_path = os.path.join(script_dir, '../bdd_essai1.db')  # Chemin relatif vers la base de données

        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # Récupérer tous les noms de tables dans la base de données
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in c.fetchall()]

        # Parcourir chaque table pour supprimer ses données
        for table in tables:
            # Exclure les tables système comme sqlite_sequence
            if table == "sqlite_sequence":
                continue

            # Supprimer les données
            print(f"Suppression des données de la table {table}...")
            c.execute(f"DELETE FROM {table};")

            # Réinitialiser l'auto-incrémentation si applicable
            c.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

        # Confirmer les changements
        conn.commit()
        print("Toutes les données ont été supprimées et les IDs réinitialisés.")
    except Exception as e:
        print(f"Erreur lors de la suppression des données : {e}")
    finally:
        # Fermer la connexion
        conn.close()

# Appeler la fonction
if __name__ == '__main__':
    supprimer_donnees_toutes_tables()
