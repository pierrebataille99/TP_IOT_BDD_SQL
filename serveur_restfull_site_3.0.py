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




# @app.route('/camembert')
# def camembert_page():
#     return render_template('camembert.html')

# # Une autre route pour des données spécifiques (par exemple, en JSON)
# @app.route('/camembert/<logement_id>')
# def camembert_data(logement_id):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT type_facture, SUM(montant) as total_montant
#             FROM Facture
#             WHERE LOGEMENT_ID = ?
#             GROUP BY type_facture
#         """, (logement_id,))
#         factures = cursor.fetchall()
#         conn.close()

#         data = [(row[0], row[1]) for row in factures]
#         return render_template('camembert.html', data=data)
#     except sqlite3.OperationalError as e:
#         return jsonify({'error': f'Erreur avec la base de données : {str(e)}'}), 500


@app.route('/camembert/<logement_id>')
def camembert(logement_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Requête SQL pour regrouper les données par type de facture
        cursor.execute("""
            SELECT type_facture, SUM(montant) as total_montant
            FROM Facture
            WHERE LOGEMENT_ID = ?
            GROUP BY type_facture
        """, (logement_id,))
        
        factures = cursor.fetchall()
        conn.close()

        # Transformez les résultats en une liste utilisable pour le camembert
        data = [(row[0], row[1]) for row in factures]

        # Rendez le graphique avec les données
        return render_template('camembert.html', data=data)
    except sqlite3.OperationalError as e:
        return jsonify({'error': f'Erreur avec la base de données : {str(e)}'}), 500
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








#main

if __name__ == '__main__':
    app.run(debug=True)
