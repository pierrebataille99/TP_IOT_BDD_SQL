#############################################   Code de Pierre BATAILLE    #############################################

import sqlite3
from flask import Flask, jsonify, render_template_string, request, render_template
import requests
from collections import defaultdict
from datetime import datetime


app = Flask(__name__)
#serveur flask
# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bdd_essai1.db')
    conn.row_factory = sqlite3.Row  # Permet de transformer les résultats en dictionnaires
    return conn

@app.route('/')
def home():
    #return "Welcome sur le serveur RESTful de Pierre !"
    return render_template('home.html')





###################################################################### Exercice 2.1  ###########################################################
# === PARTIE GESTION DES DONNÉES (BASE DE DONNEES) ===
# Récupérer toutes les données d'une table (GET)
@app.route('/<table_name>', methods=['GET'])         # en fonction du nom de la table
def get_all(table_name):
    try:
        conn = get_db_connection()
        query = f"SELECT * FROM {table_name}"  # Génération dynamique de la requête
        data = conn.execute(query).fetchall()
        conn.close()
        return jsonify([dict(row) for row in data]), 200
    except sqlite3.OperationalError as e:
        return jsonify({'error': f'Table {table_name} not found: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# envoyer des données en les ajoutant dans la bdd (POST)
@app.route('/<table_name>', methods=['POST'])
def add_row(table_name):
    try:
        data = request.get_json()  # Données JSON envoyées dans le corps de la requête
        if not data:
            return jsonify({'error': 'Invalid JSON format'}), 400

        conn = get_db_connection()
        
        # Génération dynamique des colonnes et des valeurs
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.keys()])
        values = tuple(data.values())
        
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        conn.execute(query, values)
        conn.commit()
        conn.close()
        return jsonify({'message': f'donnees ajoutées avec succès à {table_name}!'}), 201
    except sqlite3.OperationalError as e:
        return jsonify({'error': f'Table {table_name} not found or invalid data: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500






###################################################################### Exercice 2.2  ###########################################################
# === PARTIE GRAPHIQUE (CAMEMvBERT) ===

# @app.route('/consommation/<logement_id>')
# def consommation(logement_id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Requête SQL pour regrouper les données par type de facture
#         cursor.execute("""
#             SELECT type_facture, SUM(montant) as total_montant
#             FROM Facture
#             WHERE LOGEMENT_ID = ?
#             GROUP BY type_facture
#         """, (logement_id,))
        
#         factures = cursor.fetchall()
#         conn.close()

#         # Transformez les résultats pour le camembert
#         data = [(row["type_facture"], row["total_montant"]) for row in factures]

#         # Rendu de la page consommation.html avec les données
#         return render_template('consommation.html', data=data)
#     except sqlite3.OperationalError as e:
#         return jsonify({'error': f'Erreur avec la base de données : {str(e)}'}), 500
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



def calculer_somme_annuelle(logement_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête SQL pour calculer la somme annuelle pour chaque type de facture
        cursor.execute("""
            SELECT type_facture, SUM(valeur_consomme) as total
            FROM Facture
            WHERE LOGEMENT_ID = ?
            GROUP BY type_facture
        """, (logement_id,))
        resultats = cursor.fetchall()
        conn.close()

        # Formatage des résultats
        donnees = {row["type_facture"]: row["total"] for row in resultats}
        return donnees
    except Exception as e:
        print(f"Erreur lors du calcul des consommations annuelles : {e}")
        return {}




def calculer_factures_par_mesures(logement_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Logs pour chaque étape
        cursor.execute("SELECT * FROM Mesure LIMIT 10")
        print("Mesures :", cursor.fetchall())

        cursor.execute("SELECT * FROM Capteur_Actionneur LIMIT 10")
        print("Capteurs :", cursor.fetchall())

        cursor.execute("SELECT * FROM Type_Capteur_Actionneur LIMIT 10")
        print("Types de Capteurs :", cursor.fetchall())

        cursor.execute("SELECT * FROM Piece LIMIT 10")
        print("Pièces :", cursor.fetchall())

        # Requête pour calculer la somme des mesures par type de capteur
        query = """
            SELECT tc.nom AS type_facture, SUM(m.valeur) AS total_consommation
            FROM Mesure m
            INNER JOIN Capteur_Actionneur ca ON m.CAPTEUR_ID = ca.CAPTEUR_ID
            INNER JOIN Type_Capteur_Actionneur tc ON ca.TYPE_ID = tc.TYPE_ID
            INNER JOIN Piece p ON ca.PIECE_ID = p.PIECE_ID
            WHERE p.LOGEMENT_ID = ?
            GROUP BY tc.nom
        """
        cursor.execute(query, (logement_id,))
        consommations = cursor.fetchall()

        print(f"Consommations récupérées pour le logement {logement_id} :", consommations)

        conn.close()

        # Formatage des résultats
        factures = {row['type_facture']: round(row['total_consommation'], 2) for row in consommations}
        return factures
    except Exception as e:
        print(f"Erreur lors du calcul des factures : {e}")
        return {}











# @app.route('/consommation/<logement_id>')
# def consommation(logement_id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Requête pour récupérer les consommations avec unités et prix
#         cursor.execute("""
#             SELECT f.type_facture, SUM(f.valeur_consomme) as total_consommation, 
#                    tc.unite_mesure, SUM(f.montant) as total_prix
#             FROM Facture f
#             INNER JOIN Type_Capteur_Actionneur tc ON f.type_facture = tc.nom
#             WHERE f.LOGEMENT_ID = ?
#             GROUP BY f.type_facture, tc.unite_mesure
#         """, (logement_id,))
#         consommations = cursor.fetchall()

#         # Formatage des données pour le template
#         consommations_data = [(row["type_facture"], round(row["total_consommation"], 2), 
#                                row["unite_mesure"], round(row["total_prix"], 2)) for row in consommations]

#         conn.close()

#         return render_template('consommation.html', consommations=consommations_data)
#     except Exception as e:
#         print(f"Erreur lors de la récupération des consommations : {e}")
#         return jsonify({'error': 'Erreur lors de la récupération des données'}), 500



@app.route('/consommation/<logement_id>')
def consommation(logement_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête pour récupérer les consommations avec unités et prix
        cursor.execute("""
            SELECT f.type_facture, SUM(f.valeur_consomme) as total_consommation, 
                   tc.unite_mesure, SUM(f.montant) as total_prix
            FROM Facture f
            INNER JOIN Type_Capteur_Actionneur tc ON f.type_facture = tc.nom
            WHERE f.LOGEMENT_ID = ?
            GROUP BY f.type_facture, tc.unite_mesure
        """, (logement_id,))
        consommations = cursor.fetchall()

        # Calcul des moyennes de température et d'humidité
        cursor.execute("""
            SELECT AVG(m.valeur) AS moyenne, tc.nom AS type
            FROM Mesure m
            INNER JOIN Capteur_Actionneur ca ON m.CAPTEUR_ID = ca.CAPTEUR_ID
            INNER JOIN Type_Capteur_Actionneur tc ON ca.TYPE_ID = tc.TYPE_ID
            WHERE tc.nom IN ('Capteur Température', 'Capteur Humidité')
            AND ca.PIECE_ID IN (SELECT PIECE_ID FROM Piece WHERE LOGEMENT_ID = ?)
            GROUP BY tc.nom
        """, (logement_id,))
        moyennes = cursor.fetchall()

        conn.close()

        # Formatage des données pour le template
        consommations_data = [(row["type_facture"], round(row["total_consommation"], 2), 
                               row["unite_mesure"], round(row["total_prix"], 2)) for row in consommations]
        moyennes_data = {row["type"]: round(row["moyenne"], 2) for row in moyennes}

        return render_template(
            'consommation.html', 
            consommations=consommations_data, 
            moyennes=moyennes_data
        )
    except Exception as e:
        print(f"Erreur lors de la récupération des consommations : {e}")
        return jsonify({'error': 'Erreur lors de la récupération des données'}), 500










@app.route('/consommation/<logement_id>', methods=['GET'])
def api_calculer_factures(logement_id):
    factures = calculer_factures_par_mesures(logement_id)
    return jsonify(factures), 200
























###################################################################### Exercice 2.3  ###########################################################

# === PARTIE SERVEUR METEO ===


# Clé API et URL de l'API OpenWeatherMap
API_KEY = 'c4a46892b5d53ec1f0a256eff25e6834'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'


@app.route('/meteo/<ville>')
def meteo(ville):
    try:
        params = {
            'q': ville,
            'appid': API_KEY,
            'units': 'metric',
            'cnt': 40  # Prévisions pour 5 jours
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()

            # Grouper les prévisions par jour
            grouped_forecast = defaultdict(list)
            for forecast in data['list']:
                date = datetime.strptime(forecast['dt_txt'], "%Y-%m-%d %H:%M:%S").date()
                grouped_forecast[date].append({
                    'time': forecast['dt_txt'],
                    'temperature': forecast['main']['temp'],
                    'description': forecast['weather'][0]['description']
                })

            grouped_forecast = {
                str(day): forecasts for day, forecasts in grouped_forecast.items()
            }

            # Utiliser le fichier meteo.html
            return render_template('meteo.html', ville=ville, previsions=grouped_forecast)
        else:
            return jsonify({'error': 'Ville non trouvée ou erreur dans l\'API météo.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500









###################################################################### Exercice 3.0  ###########################################################

# === PARTIE site web ===



###################################################################### Partie capteurs  ###########################################################




@app.route('/capteur/<logement_id>')
def capteurs(logement_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête SQL pour récupérer les capteurs du logement
        cursor.execute("""
            SELECT 
                ca.CAPTEUR_ID AS id,
                tc.nom AS nom_capteur,
                tc.unite_mesure AS unite_mesure,
                p.nom AS nom_piece
            FROM 
                Capteur_Actionneur ca
            INNER JOIN 
                Type_Capteur_Actionneur tc ON ca.TYPE_ID = tc.TYPE_ID
            INNER JOIN 
                Piece p ON ca.PIECE_ID = p.PIECE_ID
            WHERE 
                p.LOGEMENT_ID = ?;
        """, (logement_id,))
        capteurs = cursor.fetchall()
        conn.close()

        # Formatez les données pour Jinja
        capteurs_data = [
            {
                "id": row["id"],  # ID du capteur
                "nom_capteur": row["nom_capteur"],  # Nom du capteur
                "unite_mesure": row["unite_mesure"],  # Unité de mesure
                "nom_piece": row["nom_piece"],  # Pièce associée
            }
            for row in capteurs
        ]

        # Rendre le template avec les données des capteurs
        return render_template('capteurs.html', capteurs=capteurs_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500






###################################################################### afficher les donées de la base sur el site  ###########################################################




@app.route('/données_bdd')
def afficher_toutes_les_tables():
    try:
        conn = get_db_connection()  # Assurez-vous que cette fonction pointe vers bdd_essai1.db
        cursor = conn.cursor()

        # Récupérer toutes les tables de la base de données
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        # Récupérer les données de chaque table
        toutes_les_donnees = []
        for table in tables:
            # Exclure les tables système comme sqlite_sequence
            if table == "sqlite_sequence":
                continue

            # Récupérer les colonnes
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]

            # Récupérer les données de la table
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()

            toutes_les_donnees.append({
                "table_name": table,
                "columns": columns,
                "rows": rows
            })

        conn.close()

        return render_template('données_BDD.html', toutes_les_donnees=toutes_les_donnees)
    except Exception as e:
        return f"Erreur lors de l'accès aux données : {str(e)}"







################################################# afficher graphiques capteurs  #########################""""
@app.route('/graphique_capteur/<int:capteur_id>')
def graphique_capteur(capteur_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête pour récupérer les données de mesure pour le capteur spécifique
        cursor.execute("""
            SELECT date_insertion, valeur
            FROM Mesure
            WHERE CAPTEUR_ID = ?
            ORDER BY date_insertion ASC
        """, (capteur_id,))
        donnees_mesure = cursor.fetchall()
        conn.close()

        # Transformer les données en un format exploitable pour le graphique
        donnees_graphique = [
            {"date_insertion": row[0], "valeur": row[1]}
            for row in donnees_mesure
        ]

        # Transmettre les données au template
        return render_template('graphique_capteur.html', capteur_id=capteur_id, donnees=donnees_graphique)
    except Exception as e:
        return jsonify({'error': str(e)}), 500









################################################# gestion du logement 1  #######################################


@app.route('/gestion/<logement_id>')
def gestion(logement_id):
    """
    Affiche la page de gestion des capteurs pour un logement spécifique.
    """

    print(f"Logement ID reçu : {logement_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Récupérer les pièces associées au logement
        cursor.execute("""
            SELECT PIECE_ID AS id, nom
            FROM Piece WHERE LOGEMENT_ID = ?
        """, (logement_id,))
        pieces = cursor.fetchall()

        # Récupérer les types de capteurs depuis Type_Capteur_Actionneur
        cursor.execute("""
            SELECT TYPE_ID AS id, nom
            FROM Type_Capteur_Actionneur
        """)
        types_capteurs = cursor.fetchall()

        # Récupérer les références commerciales depuis Capteur_Actionneur
        cursor.execute("""
            SELECT CAPTEUR_ID AS id, reference_commerciale
            FROM Capteur_Actionneur
        """)
        references_commerciales = cursor.fetchall()

        conn.close()

        return render_template(
            'gestion.html',
            logement_id=logement_id,
            pieces=pieces,
            types_capteurs=types_capteurs,
            references_commerciales=references_commerciales,
            message=request.args.get('message')  # Message facultatif
        )
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': str(e)}), 500





@app.route('/capteur', methods=['POST'])
def ajouter_capteur():
    """
    Ajoute un capteur avec TYPE_ID et référence commerciale à une pièce existante via API REST.
    """
    try:
        # Récupérer les données envoyées par le formulaire ou l'API
        data = request.get_json()
        type_id = data['type_id']  # TYPE_ID lié au type de capteur
        piece_id = data['piece_id']
        reference_commerciale = data['reference_commerciale']
        date_insertion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Date actuelle

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insérer le nouveau capteur dans la base de données
        cursor.execute("""
            INSERT INTO Capteur_Actionneur (TYPE_ID, reference_commerciale, PIECE_ID, date_insertion)
            VALUES (?, ?, ?, ?)
        """, (type_id, reference_commerciale, piece_id, date_insertion))
        conn.commit()
        conn.close()

        return jsonify({'message': "Nouveau capteur ajouté avec succès !"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


















    #fonction pour annuler l'autoincrement quandon on insert un nouveau capteur et pour eviter les bugs


def reset_auto_increment(table_name):
    """
    Réinitialise l'auto-incrémentation d'une table en SQLite.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
        conn.commit()
        conn.close()
        print(f"Auto-incrémentation réinitialisée pour la table {table_name}.")
    except Exception as e:
        print(f"Erreur lors de la réinitialisation de l'auto-incrémentation : {e}")





@app.route('/supprimer_capteur/<int:capteur_id>', methods=['DELETE'])
def supprimer_capteur(capteur_id):
    """
    Supprime un capteur par son ID et réinitialise la séquence d'auto-incrémentation.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Vérifie si le capteur existe avant de le supprimer
        cursor.execute("SELECT * FROM Capteur_Actionneur WHERE CAPTEUR_ID = ?", (capteur_id,))
        capteur = cursor.fetchone()
        if not capteur:
            return jsonify({'error': f"Capteur avec ID {capteur_id} introuvable."}), 404

        # Supprime le capteur
        cursor.execute("DELETE FROM Capteur_Actionneur WHERE CAPTEUR_ID = ?", (capteur_id,))
        conn.commit()

        # Réinitialise la séquence
        reset_auto_increment('Capteur_Actionneur')

        conn.close()
        return jsonify({'message': f"Capteur avec ID {capteur_id} supprimé avec succès."}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500























@app.route('/test', methods=['POST', 'GET'])
def test_donnees():
    if request.method == 'POST':
        # Récupérer les données JSON envoyées par l'ESP
        data = request.json
        if not data:
            return jsonify({'error': 'Pas de données reçues ou format invalide'}), 400

        # Afficher les données dans la console Flask
        print(f"Données reçues : {data}")

        return jsonify({'message': 'Données reçues avec succès !', 'data': data}), 201

    elif request.method == 'GET':
        # Retourne une réponse pour vérifier que le serveur fonctionne
        return jsonify({'message': 'Serveur en ligne et prêt pour les tests !'}), 200
















@app.route('/Mesure', methods=['POST'])
def ajouter_mesure():
    try:
        data = request.json
        if not data or 'CAPTEUR_ID' not in data or 'valeur' not in data:
            return jsonify({'error': 'Format JSON invalide'}), 400

        # Extraire les données
        capteur_id = data['CAPTEUR_ID']
        valeur = data['valeur']
        date_insertion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO Mesure (CAPTEUR_ID, valeur, date_insertion)
            VALUES (?, ?, ?)
        """, (capteur_id, valeur, date_insertion))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Mesure ajoutée avec succès'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


















#main

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

