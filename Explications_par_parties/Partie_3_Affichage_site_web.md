la base du site html est incluse dns **base.html**: il y a a base de navigation, l'interface globale du site et le footer (en bas)
- **base.html** est donc un template qui est inclus dans tous les autres templates

- **home.html** est un template qui est inclus dans **base.html** et qui contient la page d'accueil

- **capteurs.html** est un template qui est inclus dans **base.html** et qui contient toute les infos des 6 capteurs de la base

- **consommation.html** est un template qui est inclus dans **base.html** et qui contient toute les infos de la consommation des mesures des 6 capteurs

- **donnees_BDD.html** est un template qui est inclus dans **base.html** et qui affiche TOUTES les données de la base de données **bdd_essai1.db**

- **gestion.html** est un template qui est inclus dans **base.html** et qui permet d'ajouter ou de dupprimer des capteurs au besoin (via leur ID)

- **graphique_capteur.html** est un template qui est inclus dans **base.html** et qui est lié au fichier **capteur.html** et qui permet de visualiser les données de chaque capteur avec un ggraphique lorsq'uon clique dessus.

-**meteo.html** est un template qui est inclus dans **base.html** et qui affiche la meteo pour une ville donnée (à saisir dans la barre d'URL)





le fichier **serveur_restfull_site_3_8.py** est le fichier principal qui permet de lancer le serveur et de faire fonctionner tout le site. c'est le serveur flask qui contient toute les APP routes indispensables pour faire fonctionner tout le site, (liées dans la barre de navigation sur tous les onglets)

Le fichier **styles.css** contient toutes les infos de styles à appliquer à la page web


