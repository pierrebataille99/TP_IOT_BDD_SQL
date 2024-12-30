# TP_IOT_BDD_SQL


Pour visualiser le site web en local:
il suffit d'executer avec python le fichier serveur_restfull_site_3_8
Puis d'aller sur le navigateur et d'aller à l'adresse suivante: http://127.0.0.1:5000/
Vous pourrez naviguer sur mon site web en local


Voici le contenu de mes fichiers:


# Dans le dossier /Envoi_temp_arduino/
# *Envoi_temp_arduino.ino*:

    Ce prrogramme Arduino récupère les données de température et d'humidité de l'ESP8266 avec le DHT11:
    celui-ci envoie ces données vers la base de données dans les mesures des capteurs ID 5 et 6



# Dans le dossier /Envoi_temp_arduino/
# *erase_all_donnes.py*
    Ce programme supprime toute les données des tables de la base de données

# *Remplissage_all_donnees.py*
    Ce programme remplit les tables de la base de données avec des données aléatoires (sauf pour les capteurs 5 et 6 qui sont remplis avec des données réelles issues de l'ESP)





# Dans le dossier /Static/
# *scripts.js*
    Ce script JavaScript permet de récupérer les données de la base de données et de les afficher

# *style.css*
    Ce fichier CSS permet de personnaliser l'apparence du site web 



# Dans le dossier /templates/
# *base.html*
    ce fichier HTML est le template principal du site web, il contient les éléments de base comme la
    barre de navigation et la section de contenu


# *capteurs.html*
    ce fichier HTML permet de visualiser les données des capteurs sous formes de données (ID, typ, ..) et de graphiques (température, humidité, consommation) --> voir fichier # *graphique_capteur.html*

# *consommation.html*
    ce fichier HTML permet de visualiser les données de consommation du logement sous forme de graphique et
    de tableau.  Il permet de voir la facture de prix en fonction de la consommation issues des mesurse pour chaque capteur

# *donnees_BDD.html*
    ce fichier HTML permet de visualiser les données de toute la base de données sous forme de tableau 

# *gestion.html*
    ce fichier HTML permet de gérer les capteurs (ajout, suppression)

# *graphique_capteur.html*
    ce fichier HTML permet de visualiser les données d'un capteur sous forme de graphique pour chaque capteur

# *home.html*
    ce fichier permet d'afficher la page d'accueil du site

# *meteo.html*
    ce fichier petmet d'afficher la meteo (via l'API) pour une ville donnée (à rentrrer dans l'url)






# Dans le dossier parent
# *bdd_essai1.db*
    c'est la base de donnée de tout le projet , elle contient toutes les données de toutes les tables du *logement.sql*

# *Liste commandes Curl.txt*
    Liste des commances POST utilisées dans Postman pour envoyer des données dans la base de données

# *remplissage.py*
    premier fichier demandé dans le TP pour faire un replissage de la base de données
    je n'ai utilisé çà qu'au début, apres j'ai utilisé le fichier dans /remplissage_erase/ pour ecrire des données dans la base

# *serveur_restfull_site_3_8*
    c'est le fichier principal du serveur restfull qui contient toutes les App Rout du serveur flask ainsi que toutes lss fonctions pour les requetes POST, GET, et le calcul des données










**Sources**:
J'ai utilisé plusieurs sites et livres et videos:

videos sur le html:
https://www.youtube.com/watch?v=68oSyuKVjeU&ab_channel=FromScratch-Led%C3%A9veloppementWebdez%C3%A9ro
https://www.youtube.com/watch?v=p6uF-p_x94k&ab_channel=CommentCoder

pour les graphiques camenberts: (adaptés aussi en graphs classiques) 
https://developers.google.com/chart/

j'ai utilisé beaucoup ChatGpT principalement pour le HTML/CSS/JS et des squelettes  de code pour lier la base de données au site web. Egalement pour debug certains problèmes SQL/.DB
car je n'ai jamais appris ces langages, et il m'était impossible d'apprendre ces langages en simplement 4 TP
J'ai surtout utilisé dans le but d'apprendre plutot que l'IA fasse tout à ma place, en utilisant GPT intelligeament
Et de fait j'ai passé plus de 25h chez moi en plus des TP pour faire fonctionner mon petit site.
Et en effet j'ai apprs beaucoup de choses sur les langages et sur les bases de données et sur les requetes HTTP et sur les API.
JE suis satisfait de mon travail.


Quelques prompts:

https://chatgpt.com/share/6772db52-1a64-8006-80e2-8bf5abb58591

exemples de prompts donnés:


"je veux faire une petite appli Flask qui se connecte à une base SQLite. montremoi comment recup toutes les données d’une table et comment en ajouter avec une requête POST ?"

"je veux un formulaire HTML qui envoie des infos à Flask pour ajouter des capteurs à une base. donne moi un exemple simple avec un POST "


Quelques sources stackoverflox:
https://stackoverflow.com/questions/1210664/no-module-named-sqlite3
https://stackoverflow.com/questions/23567094/how-can-i-get-data-from-database-into-html-table/23567337#23567337


autres liens un peu utilisés:
https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
https://www.w3schools.com/sql/sql_insert.asp
https://pythonspot.com/flask-json-and-the-google-charts-api/



Pour résumer, j'ai utilisé plus GPT que des ressources en lignes. GPT est super outil pour apprendre, et çà m'a permis d'apprendre plein de choses sur les bdd, le sql et HTML/CSS. J'ai aussi appris à utiliser Flask et à faire des requetes HTTP. J'ai utilisé GPT pour apprendre et non pour qu'il le fasse à ma place: l'IOT m'interesse beaucoup, c'est pourquoi j'ai aimé m'investir dans ce projet. En plus, j'ai l'intention de me créeer mon site web d'affichage de photos, ces acquis de ce projet me serviront de bonne base pour démarrer.

