from flask import Flask, request, jsonify

import sqlite3

app = Flask(__name__)

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('bdd_essai1.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "welcome sur le serveur RESTful hahahaha !"

# Récupérer toutes les mesures
@app.route('/mesures', methods=['GET'])
def get_mesures():
    conn = get_db_connection()
    mesures = conn.execute('SELECT * FROM Mesure').fetchall()
    conn.close()
    return jsonify([dict(m) for m in mesures])

# Ajouter une nouvelle mesure
@app.route('/mesures', methods=['POST'])
def add_mesure():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Mesure (CAPTEUR_ID, valeur, date_insertion) VALUES (?, ?, ?)',
        (data['CAPTEUR_ID'], data['valeur'], data.get('date_insertion', None))
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Mesure ajoutée avec succès!'}), 201

# Récupérer les factures
@app.route('/factures', methods=['GET'])
def get_factures():
    conn = get_db_connection()
    factures = conn.execute('SELECT * FROM Facture').fetchall()
    conn.close()
    return jsonify([dict(f) for f in factures])

# Ajouter une nouvelle facture
@app.route('/factures', methods=['POST'])
def add_facture():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO Facture (LOGEMENT_ID, type_facture, date_facture, montant, valeur_consomme) VALUES (?, ?, ?, ?, ?)',
        (data['LOGEMENT_ID'], data['type_facture'], data['date_facture'], data['montant'], data['valeur_consomme'])
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Facture ajoutée avec succès!'}), 201

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Flask fonctionne correctement !"

# if __name__ == "__main__":
#     app.run(debug=True)
