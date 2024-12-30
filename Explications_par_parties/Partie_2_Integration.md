Dans cette partie j'ai remplisla base de données avec le remplissage.py au début, puis j'ai utilisé postman pour faire des requetes POST:
L'idée était de remplir certaines données de la base de données via des requetes POST, mais j'ai réalisé que cela n'était pas suffisant pour remplir la base car il fallait faire une donnée par une. le but etait de maitriser les requetes GET et POST car par la suite je serai obligé  d'utiliser des get et post sur le site internet pour envoyer et recevoir les données.

J'ai mis dan le fichier *Liste commandes Curl.txt* les différentes commandes CURL en GET et POST pour envoyer et recevoir des données de la bse de données.


J'ai ensuite fait fonctionner mon ESP8266 ave cun capteur DHT11 de temperature / humidite
Cet ESP via un programme Arduino: *Envoi_temp_arduino.ino* a envoyé les données de température et d'humidité à la base de données, via des requets POST avec retour code 200

J'ai également fait un graphique en camenbert pour les factures en fonction du prix et des consommation respectives.
Ce graphique, je l'ai fait dans un premier temps via le template google. cela focntionnait
Puis j'ai décidé de ne pas utiliser de modèle camembert car moins adapté à mes besoins: j'ai pris un graphique plus conventionnel en barres. (au besoin je peux montrer à l'evaluateur que mon graphique en camenbert fonctionne)

le graphique affiché sur le site web est inclu dans le fihcier *consommation.html*


Egalement dans le fichier *meteo.html* j'ai utilisé une API gratuite qui permet d'afficher la meteo d'une ville donnée, en fonction d'une clé. Cela fonctionne, vous pouvez le voir sur le site ne local


