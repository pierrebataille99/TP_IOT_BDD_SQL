from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Route GET pour tester si le serveur est en ligne
@app.route('/test', methods=['GET'])
def test_serveur():
    return jsonify({"message": "Serveur en ligne et prêt pour les tests !"})

# Route POST pour recevoir les données de l'ESP8266
@app.route('/test', methods=['POST'])
def recevoir_donnees():
    try:
        data = request.json  # Récupère les données JSON envoyées
        temperature = data.get("temperature")

        if not temperature:  # Vérifie si les données sont présentes
            return jsonify({"error": "Température manquante"}), 400

        # Connexion à la base de données SQLite
        conn = sqlite3.connect('bdd_essai1.db')
        cursor = conn.cursor()

        # Insertion des données dans la table 'Mesure'
        cursor.execute("""
            INSERT INTO Mesure (id_capteur_actionneur, valeur, date_insertion) 
            VALUES (?, ?, datetime('now'))
        """, (5, temperature))  # ID 5 pour le capteur de température

        conn.commit()
        conn.close()

        print("Données reçues :", data)
        return jsonify({"message": "Données insérées avec succès dans la BDD", "data": data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route GET pour afficher les dernières données de température
@app.route('/afficher_donnees', methods=['GET'])
def afficher_donnees():
    try:
        conn = sqlite3.connect('bdd_essai1.db')
        cursor = conn.cursor()

        # Sélectionner les 10 dernières températures
        cursor.execute("""
            SELECT valeur, date_insertion 
            FROM Mesure 
            WHERE id_capteur_actionneur = 5 
            ORDER BY date_insertion DESC 
            LIMIT 10
        """)
        mesures = cursor.fetchall()
        conn.close()

        # Retourner les données sous forme JSON
        return jsonify({
            "mesures": [{"temperature": m[0], "date": m[1]} for m in mesures]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Point d'entrée principal
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
