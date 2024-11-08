import sqlite3, random

# ouverture/initialisation de la base de donnee 
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# A completer...

# fermeture
conn.commit()
conn.close()





