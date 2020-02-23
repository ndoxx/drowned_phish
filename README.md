# drowned_phish
A small tool I made to flood phishers' databases with fake but credible information.

Fake credentials are generated from several lists of names, pseudonyms and addresses. I use *crazyjunkie*'s generator to create valid credit card numbers that pass the MOD 10 check. This tool is programmed to generate plausible __FRENCH__ credentials, but it should be easy enough to adapt for any other country. drowned_phish comes with two actual scammer profiles I used during development. The codebase is not that great at the moment, because well... I'm no Python expert.

##Features:
- Fake credentials are plausible, credit card numbers pass the MOD 10 check
- Downloads a proxy list on program startup, a proxy is chosen at random before each attempt
- Multithreaded mode for faster flooding
- Stealth mode with random delays

##Third party:
crazyjunkie's credit card number generator:
[a link](https://github.com/eye9poob/python/blob/master/credit-card-numbers-generator.py)


# drowned_phish [FR]
Un outil que j'ai codé pour pourrir les bases de données de phishers, avec des informations fausses mais crédibles.

Les fausses informations sont générées depuis plusieurs listes de noms, pseudonymes et adresses. J'utilise le générateur de *crazyjunkie* pour créer des numéros de carte de crédit valides, qui passent le test MOD 10. drowned_phish vient livré avec deux profiles d'arnaqueurs que j'ai utilisés lors du développement. Le code est loin d'être élégant pour le moment, je n'ai après tout que peu d'expérience avec Python.

##Fonctionnalités:
- Les fausses informations sont plausibles, les numéros de carte de crédit passent le test MOD 10
- Une liste de proxies est téléchargée au démarrage, un proxy est sélectionné au hasard avant chaque connexion
- Mode multithreadé pour une attaque plus rapide
- Mode ninja avec délais aléatoires

##Third party:
Générateur de numéros de carte de crédit par crazyjunkie:
[a link](https://github.com/eye9poob/python/blob/master/credit-card-numbers-generator.py)


##Screenshots:
![Target acquired](screenshots/0_scam_website.png?raw=true "Target acquired")
![Sniff HTTP request](screenshots/1_POST_headers_and_data.png?raw=true "Sniff HTTP request")
![Pwned](screenshots/2_pwned.png?raw=true "Pwned")
