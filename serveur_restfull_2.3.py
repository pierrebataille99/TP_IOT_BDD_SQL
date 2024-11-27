#############################################   Code de Pierre BATAILLE    #############################################

import sqlite3
from flask import Flask, jsonify, render_template_string, request
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
    return "Welcome sur le serveur RESTful de Pierre !"





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


# Template HTML pour Google Charts
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Camembert Google Charts</title>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Type de Facture', 'Montant (€)'],
          {% for label, value in data %}
            ['{{ label }}', {{ value }}],
          {% endfor %}
        ]);

        var options = {
          title: 'Répartition des Factures par Type',
          is3D: true,
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <h1>Répartition des Factures par Type</h1>
    <div id="piechart" style="width: 900px; height: 500px;"></div>
  </body>
</html>
"""






# Récup les factures par type pour un logement 
@app.route('/camembert/<logement_id>', methods=['GET'])
def camembert(logement_id):
    try:
        conn = get_db_connection()
        
        # regrouper les facture par type + somme des montants
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type_facture, SUM(montant) as total_montant
            FROM Facture
            WHERE LOGEMENT_ID = ?
            GROUP BY type_facture
        """, (logement_id,))
        
        factures = cursor.fetchall()
        conn.close()

        # Formater les data pour le graphique
        data = [(row[0], row[1]) for row in factures]

        # Générer  le graphique
        return render_template_string(HTML_TEMPLATE, data=data)
    except sqlite3.OperationalError as e:
        return jsonify({'error': f'Factures pour LOGEMENT_ID={logement_id} introuvables: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

















###################################################################### Exercice 2.3  ###########################################################

# === PARTIE SERVEUR METEO ===





# # Clé API et URL de l'API OpenWeatherMap
# API_KEY = 'c4a46892b5d53ec1f0a256eff25e6834'        #donné par l'aPI
# BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# @app.route('/meteo/<ville>', methods=['GET'])
# def get_meteo(ville):
#     """
#     Récupère les prévisions météo à 5 jours pour une ville donnée.
#     """
#     try:
#         # requête vers l'API OpenWeatherMap
#         params = {
#             'q': ville,
#             'appid': API_KEY,
#             'units': 'metric',  # Pour des données en degrés Celsius
#             'cnt': 40  # Nombre de prévisions (5 jours), toutes les  3heures
#         }
#         response = requests.get(BASE_URL, params=params)

#         # Vérifier si la requête a réussi
#         if response.status_code == 200:
#             data = response.json()

#             # 
#             # prévisions pour les 5 jours
#             previsions = [
#                 {
#                     'date': forecast['dt_txt'],
#                     'temperature': forecast['main']['temp'],
#                     'description': forecast['weather'][0]['description']
#                 }
#                 for forecast in data['list']
#             ]

#             return jsonify({'ville': ville, 'previsions': previsions}), 200
#         else:
#             return jsonify({'error': 'Ville non trouvée ou erreur dans l\'API météo.'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500











# Clé API et URL de l'API OpenWeatherMap
API_KEY = 'c4a46892b5d53ec1f0a256eff25e6834'
BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'

@app.route('/meteo/<ville>', methods=['GET'])
def get_meteo(ville):
    """
    Récupère les prévisions météo à 5 jours pour une ville donnée (toutes les 3 heures),
    et les regroupe par jour.
    """
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

            return jsonify({'ville': ville, 'previsions': grouped_forecast}), 200
        else:
            return jsonify({'error': 'Ville non trouvée ou erreur dans l\'API météo.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/interface/<ville>')
def meteo_interface(ville):
    """
    Interface HTML pour afficher les prévisions météo d'une ville.
    """
    params = {
        'q': ville,
        'appid': API_KEY,
        'units': 'metric',
        'cnt': 40
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

        # HTML et CSS intégrés directement dans le code Python
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prévisions météo - {{ ville }}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: #f4f4f4;
                }
                .container {
                    max-width: 800px;
                    margin: 20px auto;
                    padding: 20px;
                    background: #fff;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }
                h1 {
                    text-align: center;
                    color: #333;
                }
                .forecast-container {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }
                .day-forecast {
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 10px;
                    background: #f9f9f9;
                }
                .day-forecast h2 {
                    margin: 0 0 10px;
                    color: #555;
                    font-size: 1.2em;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 5px;
                }
                .day-forecast ul {
                    list-style: none;
                    padding: 0;
                }
                .day-forecast li {
                    display: flex;
                    justify-content: space-between;
                    padding: 5px 0;
                    border-bottom: 1px solid #eee;
                }
                .day-forecast li:last-child {
                    border-bottom: none;
                }
                .time {
                    font-weight: bold;
                    color: #444;
                }
                .temp {
                    color: #e63946;
                }
                .desc {
                    font-style: italic;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Prévisions météo pour {{ ville }}</h1>
                <div class="forecast-container">
                    {% for day, forecasts in previsions.items() %}
                    <div class="day-forecast">
                        <h2>{{ day }}</h2>
                        <ul>
                            {% for forecast in forecasts %}
                            <li>
                                <span class="time">{{ forecast.time.split(' ')[1] }}</span>
                                <span class="temp">{{ forecast.temperature }}°C</span>
                                <span class="desc">{{ forecast.description }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </body>
        </html>
        """
        return render_template_string(html, ville=ville, previsions=grouped_forecast)
    else:
        return f"Erreur : Impossible de trouver la ville {ville}", 404












































#main

if __name__ == '__main__':
    app.run(debug=True)
