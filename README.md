# arXivWatch

Un script Python élémentaire pour suivre les mises à jours sur arXiv, dans des domaines spécifiques.

## Prérequis
python >= 3 avec les modules beautifulsoup4, requests, smtplib, jinja2.

## Usage
Le script effectue les opérations suivantes :

1. récupère les flux rss d'arXiv correspondant aux _sujets_ voulus, en s'arrêtant à la date de la dernière mise à jour,
2. filtre selon des _critères_ définits par l'usager,
3. envoie un email synthétique à l'adresse mail voulue.

Il est destiné à être lancé régulièrement par cron, ou être placé dans les scripts de NetworkManager.

### Subjets et filtre
- Les _sujets_ téléchargés (classifications arXiv, e.g. math.KT, math.OA) peuvent être choisis en modifiant la variable `subjects` dans l'en-tête du script.
- Les _critères_ du filtre sont définis par la fonction `is_interesting`, également dans l'en-tête du script.

### Paramètres mail
Tous les paramètres relatifs aux adresses emails sont renseignés dans le script. Le script est destiné à un usage personnel : le mot de passe étant écrit en clair dans le fichier, la sécurité est minimale.

## Documentation
Le script utilise [l'API arXiv](https://arxiv.org/help/api/user-manual).
  
