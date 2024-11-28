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






@app.route('/consommation/<logement_id>')
def consommation(logement_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête SQL pour les montants
        cursor.execute("""
            SELECT type_facture, SUM(montant) as total_montant
            FROM Facture
            WHERE LOGEMENT_ID = ?
            GROUP BY type_facture
        """, (logement_id,))
        factures_montant = cursor.fetchall()

        # Requête SQL pour les valeurs consommées
        cursor.execute("""
            SELECT type_facture, SUM(valeur_consomme) as total_consommation
            FROM Facture
            WHERE LOGEMENT_ID = ?
            GROUP BY type_facture
        """, (logement_id,))
        factures_consommation = cursor.fetchall()

        conn.close()

        # Transformez les résultats en listes
        data_montant = [(row["type_facture"], row["total_montant"]) for row in factures_montant]
        data_consommation = [(row["type_facture"], row["total_consommation"]) for row in factures_consommation]

        # Passez les deux jeux de données au template
        return render_template('consommation.html', data_montant=data_montant, data_consommation=data_consommation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500











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
                p.nom AS nom_piece,
                l.LOGEMENT_ID AS logement_id
            FROM 
                Capteur_Actionneur ca
            INNER JOIN 
                Type_Capteur_Actionneur tc ON ca.TYPE_ID = tc.TYPE_ID
            INNER JOIN 
                Piece p ON ca.PIECE_ID = p.PIECE_ID
            INNER JOIN 
                Logement l ON p.LOGEMENT_ID = l.LOGEMENT_ID
            WHERE 
                l.LOGEMENT_ID = ?;
        """, (logement_id,))
        capteurs = cursor.fetchall()
        conn.close()

        # Formatez les données pour Jinja
        capteurs_data = [
            {
                "id": row["id"],  # Ajout de l'ID du capteur
                "nom_capteur": row["nom_capteur"],
                "unite_mesure": row["unite_mesure"],
                "nom_piece": row["nom_piece"]
            }
            for row in capteurs
        ]

        # Rendre le template capteurs.html
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












































# @app.route('/test_table/<table_name>')
# def test_table(table_name):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Récupérer les colonnes de la table
#         cursor.execute(f"PRAGMA table_info({table_name})")
#         columns = [col[1] for col in cursor.fetchall()]

#         # Récupérer les données de la table
#         cursor.execute(f"SELECT * FROM {table_name}")
#         rows = cursor.fetchall()

#         conn.close()

#         # Convertir les données pour affichage
#         result = f"<h1>Table : {table_name}</h1>"
#         result += f"<h2>Colonnes : {', '.join(columns)}</h2>"
#         result += "<h3>Données :</h3><table border='1'><tr>"

#         # Ajouter les colonnes dans le tableau
#         for col in columns:
#             result += f"<th>{col}</th>"
#         result += "</tr>"

#         # Ajouter les lignes dans le tableau
#         for row in rows:
#             result += "<tr>"
#             for cell in row:
#                 result += f"<td>{cell}</td>"
#             result += "</tr>"
#         result += "</table>"

#         return result
#     except Exception as e:
#         return f"Erreur pour la table {table_name} : {str(e)}"








#main

if __name__ == '__main__':
    app.run(debug=True)
