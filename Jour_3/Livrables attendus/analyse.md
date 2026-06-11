# RAPPORT DE JOUR 3

## 3. Analyse comparative : Avant / Après sécurisation

### Scénario d'attaque par Injection SQL rejoué
L'attaque consiste à injecter la charge utile suivante dans le champ d'authentification de l'interface utilisateur :
* **Nom d'utilisateur (Username) :** `admin' --`
* **Mot de passe (Password) :** `n_importe_quoi`

### Tableau comparatif technique des comportements applicatifs

| Critère d'évaluation | Statut au Jour 2 (Application Vulnérable) | Statut au Jour 3 (Application Sécurisée) |
| :--- | :--- | :--- |
| **Mécanisme interne de requête** | Concaténation de chaînes de caractères dynamiques :<br>`"SELECT * FROM users WHERE username = '" + user + "' AND password = '" + pwd + "'"` | Requête préparée (paramétrée) via l'interpréteur de pilotes PostgreSQL :<br>`"SELECT id, username, password, email FROM users WHERE username = %s;"` |
| **Interprétation de la charge utile** | Le caractère `'` ferme prématurément la chaîne SQL. Les caractères `--` transforment le reste de la requête d'origine en commentaire, neutralisant la vérification du mot de passe. | La totalité de l'entrée `admin' --` est encapsulée de manière isolée et traitée purement comme une chaîne de caractères littérale (Donnée brute). |
| **Résultat de l'authentification** | **Accès accordé** : Le serveur renvoie le premier utilisateur correspondant au profil (compte `admin`), sans validation de mot de passe. | **Accès refusé** : L'application recherche un utilisateur possédant précisément le pseudonyme complet `admin' --`. |
| **Message retourné à l'écran** | Redirection vers l'espace d'administration ou affichage des données sensibles du compte ciblé. | Affichage d'une notification d'erreur générique : *"Identifiant ou mot de passe incorrect"*. |
| **Stockage des mots de passe** | **Clair** : Les secrets des utilisateurs sont visibles en texte brut dans la table PostgreSQL (`admin123`, `alice123`). | **Haché de manière irréversible** : Les secrets sont transformés en empreintes uniques via l'algorithme robuste `Bcrypt`. |
| **Résilience face au vol de base de données (Dump)** | Compromission totale et immédiate de l'intégrité de l'ensemble des comptes de la plateforme. | Protection cryptographique forte. Les mots de passe restent illisibles, protégés contre les attaques par force brute et par dictionnaires. |

---

## 4. Captures d'écran et validations visuelles de l'infrastructure

> 💡 **Instructions pour la composition finale :** Remplacer les encadrés ci-dessous par vos captures d'écran correspondantes pour finaliser votre dossier de livrables.


### B. Logs d'audit générés en console (Audit de sécurité)
Interception en temps réel des flux applicatifs au sein du terminal de commande de votre Mac. On constate la distinction explicite entre une connexion validée et un blocage d'injection SQL (`admin' --`).
```
┌───────────────────────────────────────────────────────────────────────────┐
│ [ PLACER LA CAPTURE ÉCRAN ICI ]                                           │
│ Fichier source : Screenshot 2026-06-10 at 11.29.01.png                    │
│ Contenu : Terminaux avec [INFO] CONNEXION_REUSSIE et [WARNING] ECHEC...  │
└───────────────────────────────────────────────────────────────────────────┘
```

### C. Déploiement de l'infrastructure de supervision (Grafana / Loki)
Validation de la configuration de l'infrastructure DevOps. La source de données Loki a été ajoutée avec succès au serveur Grafana centralisé, validant la syntaxe d'analyse de requêtes complexes LogQL.
```
┌───────────────────────────────────────────────────────────────────────────┐
│ [ PLACER LA CAPTURE ÉCRAN ICI ]                                           │
│ Fichier source : Screenshot 2026-06-10 at 11.33.48.jpg                    │
│ Contenu : Onglet Explore de Grafana affichant la requête LogQL valide     │
└───────────────────────────────────────────────────────────────────────────┘
```

### D. Supervision de l'état des conteneurs système
Supervision opérationnelle du cycle de vie des conteneurs isolés au sein de l'architecture Docker Desktop de votre Mac (PostgreSQL, Grafana, Loki).
```
┌───────────────────────────────────────────────────────────────────────────┐
│ [ PLACER LA CAPTURE ÉCRAN ICI ]                                           │
│ Fichier source : Screenshot 2026-06-10 at 11.29.17.jpg                    │
│ Contenu : Tableau de bord Docker Desktop confirmant le statut des microserv│
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Réponses aux questions d'analyse technique

### Q1. Pourquoi l'injection SQL `admin' --` ne fonctionne-t-elle plus avec une requête préparée ?
**Réponse :** Dans une requête paramétrée ou préparée, la structure logique de l'instruction SQL est pré-compilée par le serveur de base de données avant que les entrées de l'utilisateur ne soient injectées. Les valeurs fournies par l'utilisateur (ici `admin' --`) sont transmises séparément du code exécutable de la requête. 

Les métacaractères SQL, tels que le guillemet simple `'` (utilisé pour fermer un champ de texte) ou le double tiret `--` (utilisé pour initier un commentaire), perdent leur sémantique de contrôle. Ils sont traités de manière stricte comme de simples données littérales de type texte. Par conséquent, le moteur SQL recherche un utilisateur dont le nom de compte est textuellement et exactement égal à `admin' --`, ce qui neutralise définitivement la faille de sécurité.

### Q2. Quel est l'intérêt du hachage avec Bcrypt par rapport à un hachage simple comme MD5 ou SHA-256 ?
**Réponse :** Les algorithmes classiques comme MD5 ou SHA-256 ont été conçus à des fins de rapidité et d'intégrité de transfert de données. Un système moderne équipé de cartes graphiques performantes (GPU) ou disposant de dictionnaires précalculés géants (*Rainbow Tables*) peut tester des dizaines de milliards de combinaisons MD5/SHA-256 par seconde, rendant l'attaque par force brute très efficace en cas de fuite de données.

**Bcrypt** corrige structurellement ces vulnérabilités grâce à deux fonctionnalités majeures :
1. **Un sel cryptographique aléatoire (Salt) intégré :** Il est unique pour chaque mot de passe inséré. Même si deux utilisateurs choisissent exactement le même mot de passe secret, leurs empreintes stockées en base seront totalement différentes. Cela rend obsolète l'utilisation de *Rainbow Tables*.
2. **Un facteur de coût computationnel adaptatif (Work Factor / rounds) :** Bcrypt ralentit volontairement le processus de calcul en répétant l'opération mathématique des milliers de fois (ex: `rounds=12` dans notre script). Ce décalage temporel, imperceptible pour un utilisateur unique (quelques millisecondes lors de sa connexion), s'avère fatal pour un attaquant en rendant le calcul de force brute massivement chronophage et infaisable financièrement et techniquement.

### Q3. Quelle est l'importance de différencier les niveaux de logs (`INFO`, `WARNING`, `ERROR`) dans une application en production ?
**Réponse :** La granularité des niveaux de journalisation (logs) est un pilier de la gestion opérationnelle et de la supervision d'un système informatique de production :
* **`INFO` (Niveau nominal) :** Enregistre le cycle de vie classique de la plateforme (ex: démarrage de services, déconnexions, ou authentification réussie d'Alice). Utile pour l'analyse d'activité ou l'audit d'usage légitime.
* **`WARNING` (Niveau alerte comportementale) :** Intercepte les événements inhabituels ou suspects sans pour autant bloquer le fonctionnement général de l'application (ex: un échec d'authentification avec saisie de caractères spéciaux). C'est le marqueur par excellence d'une tentative d'intrusion ou d'un brute force en cours, permettant aux équipes de sécurité (SOC) d'agir de manière préventive avant le compromis système.
* **`ERROR` / `CRITICAL` (Niveau incident majeur) :** Signale un dysfonctionnement technique bloquant au niveau de l'infrastructure (ex: déconnexion ou crash du conteneur de la base de données PostgreSQL). Ce niveau déclenche instantanément des alertes d'ingénierie automatisées (astreintes, notifications d'incident) pour une intervention immédiate.

---

## 6. Recommandations stratégiques de sécurisation applicative

Pour faire passer cette application web d'un état de prototype de TP à un standard robuste prêt pour la mise en production, l'implémentation des mesures de sécurité complémentaires suivantes est requise :

1. **Conteneurisation totale de la couche applicative (Dockerisation) :**
   * *Action :* Rédiger un fichier `Dockerfile` dédié pour l'application Flask et l'intégrer nativement à l'architecture réseau définie par le fichier `docker-compose.yml`.
   * *Bénéfice :* Cela élimine l'obligation d'exposer publiquement le port PostgreSQL (`5433`) sur la machine hôte. Les communications inter-services s'effectuent sur le port par défaut `5432` de manière totalement isolée à l'intérieur du réseau virtuel Docker.
2. **Externalisation et sécurisation de la gestion des secrets (Variables d'environnement) :**
   * *Action :* Exclure totalement les identifiants d'accès en clair (`admin` / `admin`) présents dans les codes `app.py` et `init_db.py`. Charger ces secrets via des variables d'environnement distantes ou un gestionnaire de configuration (ex: un fichier `.env` ajouté au `.gitignore`).
   * *Bénéfice :* Protection contre l'exposition ou la fuite accidentelle de clés d'administration lors du déploiement ou du partage du code sur des dépôts de type Git (GitHub, GitLab).
3. **Limitation drastique du débit de requêtes (*Rate Limiting*) :**
   * *Action :* Intégrer une couche applicative de limitation d'appels HTTP (telle que l'extension `Flask-Limiter`).
   * *Bénéfice :* Permet de bloquer temporairement une adresse IP ou un profil de compte après un seuil prédéfini de requêtes infructueuses (ex: maximum 5 tentatives de connexion par minute), neutralisant les attaques par dictionnaire automatisées.
4. **Validation et assainissement des données entrantes (*Sanitization*) :**
   * *Action :* Configurer des expressions régulières ou des bibliothèques de validation de formulaires afin de valider la structure des données transmises avant leur traitement par la couche SQL.
   * *Bénéfice :* Rejet immédiat au niveau HTTP des requêtes aberrantes contenant des métacaractères non autorisés (caractères SQL, scripts HTML ou balises JS malveillantes de type XSS).
5. **Déploiement complet d'un agent de collecte de logs (Promtail) :**
   * *Action :* Ajouter et orchestrer un conteneur *Promtail* dans le fichier `docker-compose.yml` chargé d'écouter automatiquement les flux de sortie standard de l'application Flask.
   * *Bénéfice :* Permet l'indexation dynamique, automatique et en temps réel de tous les logs d'audit au sein de l'interface Grafana Loki sans nécessiter de montages de volumes de fichiers locaux contraignants.