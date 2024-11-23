#####################################################################   Code de Pierre BATAILLE    #############################################

from flask import Flask, request, jsonify, render_template_string
import sqlite3






###################################################################### Exercice 2.1  ###########################################################
# === PARTIE GESTION DES DONNÉES (BASE DE DONNEES) ===


app = Flask(__name__)

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bdd_essai1.db')
    conn.row_factory = sqlite3.Row  # Permet de transformer les résultats en dictionnaires
    return conn

@app.route('/')
def home():
    return "Welcome sur le serveur RESTful et Camembert pour toutes les tables !"

# Récupérer toutes les données d'une table
@app.route('/<table_name>', methods=['GET'])
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

# Ajouter une nouvelle ligne dans une table
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
        return jsonify({'message': f'Data added successfully to {table_name}!'}), 201
    except sqlite3.OperationalError as e:
        return jsonify({'error': f'Table {table_name} not found or invalid data: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500







###################################################################### Exercice 2.2  ###########################################################
# === PARTIE GRAPHIQUE (CAMEMBERT) ===



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



# Récupérer les factures regroupées par type pour un logement donné
@app.route('/camembert/<logement_id>', methods=['GET'])
def camembert(logement_id):
    try:
        conn = get_db_connection()
        
        # Requête pour regrouper par type de facture et sommer les montants
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type_facture, SUM(montant) as total_montant
            FROM Facture
            WHERE LOGEMENT_ID = ?
            GROUP BY type_facture
        """, (logement_id,))
        
        factures = cursor.fetchall()
        conn.close()

        # Formater les données pour le graphique
        data = [(row[0], row[1]) for row in factures]

        # Générer et renvoyer le graphique
        return render_template_string(HTML_TEMPLATE, data=data)
    except sqlite3.OperationalError as e:
        return jsonify({'error': f'Factures pour LOGEMENT_ID={logement_id} introuvables: {str(e)}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
