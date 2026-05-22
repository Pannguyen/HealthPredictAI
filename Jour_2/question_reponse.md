# Questions / Réponses – TP SQL Injection avec Docker, Flask et PostgreSQL

## 1. Quelle est la vulnérabilité exploitée ?

La vulnérabilité exploitée est une **SQL Injection (Injection SQL)**.

Elle se produit lorsque l’application construit une requête SQL en intégrant directement les données saisies par l’utilisateur sans validation ni protection.

Dans notre application, la requête vulnérable est :

```python
query = f"""
SELECT id, username, email
FROM users
WHERE username = '{username}'
AND password = '{password}'
"""
```

Un attaquant peut injecter du code SQL dans les champs de connexion afin de modifier la requête exécutée par PostgreSQL.

---

## 2. Pourquoi l’application accepte une connexion invalide ?

La condition '1'='1' étant mathématiquement toujours vraie, la clause WHERE est validée par le moteur SQL indépendamment du mot de passe fourni, ce qui renvoie le premier enregistrement de la table (souvent le compte administrateur).

Si l'attaquant saisit ' OR '1'='1, la requête devient :


La requête générée devient :

```sql
SELECT id, username, email 
FROM users 
WHERE username = '' OR '1'='1' ...
```

Explication :

- `OR '1'='1'` est une condition toujours vraie.
- `--` transforme la suite de la requête en commentaire SQL.
- La vérification du mot de passe est donc ignorée.

L’application considère alors la requête comme valide et autorise la connexion.

---

## 3. Quelles données peuvent être compromises ?

Dans notre TP, les informations suivantes peuvent être récupérées :

- ID utilisateur
- nom d’utilisateur
- email

Selon le niveau d’accès obtenu, un attaquant pourrait également lire, modifier ou supprimer des données.

---

## 4. Cette faille vient-elle de la base de données ou de l’application ?

Le rôle de la base de données : PostgreSQL reçoit une chaîne de caractères contenant des instructions SQL et se contente de l'exécuter de manière standard. Le serveur SQL ne sait pas si la commande provient de la logique du développeur ou d'une manipulation de l'internaute.

Le rôle de l'application (la source du problème) : Le développeur a utilisé une f-string (f"...") pour fusionner des données utilisateur non vérifiées avec des commandes système. Le manque de cloisonnement entre le code (instructions SQL) et la donnée (saisie utilisateur) est l'unique cause de cette vulnérabilité.

Une implémentation sécurisée utiliserait des requêtes préparées :

```python
cur.execute(
    "SELECT * FROM users WHERE username=%s AND password=%s",
    (username, password)
)
```
---

## 5. Quels sont les risques pour une entreprise ?

Les risques pour une entreprise sont importants :

- Pertes Financières : Coûts d'investigation, frais de remédiation, amendes réglementaires (RGPD) en cas de fuite de données personnelles, pertes d'exploitation dues à un arrêt des services
- Espionnage et Sabotage : Un attaquant connecté avec un compte administrateur peut exfiltrer des secrets industriels, altérer l'intégrité des données ou paralyser l'infrastructure.
- Fuite de données sensibles
- Accès administrateur
- Modification ou suppression de données
- Interruption de service
- Non-conformité réglementaire (RGPD, ISO 27001, etc.)

Dans un environnement réel, une SQL Injection peut conduire à une compromission complète du système d’information.

---

## Conclusion

J'ai une compétence en plus qu'une mauvaise gestion des entrées utilisateur peut rendre une application vulnérable aux injections SQL.

La principale mesure de protection consiste à utiliser des **requêtes paramétrées** et à ne jamais concaténer directement les données utilisateur dans les requêtes SQL.