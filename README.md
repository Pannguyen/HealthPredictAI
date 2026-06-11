# HealthPredictAI — Sécurité des données & Gouvernance

Projet fil rouge réalisé dans le cadre du cours **Sécurité des données** (M2 Data Science).  
L'objectif est de construire une application d'authentification Flask + PostgreSQL, de la rendre volontairement vulnérable, de la sécuriser, puis de l'auditer.

---

## Structure du projet

```
HealthPredictAI/
├── Jour_1/         # Analyse RGPD et conformité (pas de code)
├── Jour_2/         # Application VULNÉRABLE (injection SQL, mots de passe en clair)
├── Jour_3/         # Application SÉCURISÉE (bcrypt, requêtes préparées, logs, Grafana)
```

---

## Stack technique

| Outil | Rôle | Port |
|---|---|---|
| **Flask** (Python) | Application web d'authentification | 5001 |
| **PostgreSQL** | Base de données utilisateurs | 5432 |
| **Docker Compose** | Orchestration de tous les services | — |
| **Prometheus** | Collecte des métriques PostgreSQL | 9090 |
| **Grafana** | Visualisation métriques et logs | 3000 |
| **Loki** | Agrégation des logs | 3100 |
| **Promtail** | Agent qui envoie les logs Flask vers Loki | 9080 |
| **postgres_exporter** | Expose les métriques PostgreSQL à Prometheus | 9187 |

---

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et **lancé**
- Python 3.11+ (pour lancer les scripts d'audit en local)

---

## Lancer le projet (Jour 3 — version sécurisée)

```bash
# 1. Aller dans le dossier
cd Jour_3

# 2. Lancer tous les services
docker compose up --build -d

# 3. Vérifier que tout est up
docker compose ps
```

### Accès aux interfaces

| Interface | URL | Identifiants |
|---|---|---|
| Application Flask | http://localhost:5001 | voir ci-dessous |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |
| Loki | http://localhost:3100 | API uniquement |

### Comptes de test

| Username | Mot de passe |
|---|---|
| admin | admin123 |
| alice | alice123 |
| bob | bob123 |

---

## Arrêter le projet

```bash
docker compose down
```

---

## Jour 2 — Version vulnérable (démonstration SQL Injection)

```bash
cd Jour_2
docker compose up --build -d
```

L'application tourne sur http://localhost:5001.  
Les mots de passe sont stockés **en clair** et les requêtes SQL sont construites par **concaténation directe** — intentionnellement vulnérable.

### Tester les injections SQL

```bash
# Depuis Jour_2 avec les conteneurs up
python3 audit.py
```

Payloads testés :
- `admin' --` → contourne la vérification du mot de passe
- `' OR '1'='1' --` → récupère tous les comptes

---

## Jour 3 — Sécurisations mises en place

### 1. Requêtes préparées (protection injection SQL)
```python
# AVANT (vulnérable)
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# APRÈS (sécurisé)
query = "SELECT id, username, password, email FROM users WHERE username = %s;"
cur.execute(query, (username,))
```

### 2. Hachage bcrypt
```python
# Création du hash (init_db.py)
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

# Vérification (app.py)
bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
```

### 3. Journalisation structurée
Trois niveaux de logs dans `app.py` :
- `INFO` — tentative de connexion initiée
- `INFO` — connexion réussie (`CONNEXION_REUSSIE`)
- `WARNING` — échec de connexion (`ECHEC_CONNEXION`)

Les logs sont écrits dans `/var/log/flask/app.log` (dans le conteneur), collectés par Promtail et envoyés à Loki.

---

## Jour 4 — Audit & Gouvernance

### Lancer le script d'audit

```bash
# Avec les conteneurs Jour_3 up
cd Jour_3
python3 audit_logs.py
```

Ce script analyse :
1. Connexions actives PostgreSQL (`pg_stat_activity`)
2. Top requêtes (`pg_stat_statements`)
3. Statistiques de la table `users`
4. Logs Flask (tentatives, succès, échecs, détection brute force)
5. Logs PostgreSQL (erreurs, tentatives d'injection)

### Configurer Grafana (première fois)

1. Aller sur http://localhost:3000 (admin/admin)
2. **Ajouter Loki** : Connections → Data Sources → Loki → URL : `http://loki:3100`
3. **Ajouter Prometheus** : Connections → Data Sources → Prometheus → URL : `http://prometheus:9090`
4. Explorer les logs Flask : Explore → Loki → `{job="APP-AUTH"}`

Queries utiles dans Grafana/Loki :
```
# Tous les logs Flask
{job="APP-AUTH"}

# Seulement les échecs
{job="APP-AUTH"} |= "ECHEC_CONNEXION"

# Seulement les succès
{job="APP-AUTH"} |= "CONNEXION_REUSSIE"
```

---

## Sauvegarde PostgreSQL

```bash
# Sauvegarder
docker exec postgres_db pg_dump -U admin tp_j2 > backup_$(date +%Y%m%d).sql

# Restaurer
cat backup_20260610.sql | docker exec -i postgres_db psql -U admin -d tp_j2
```

---

## Fichiers importants

| Fichier | Description |
|---|---|
| `app.py` | Application Flask principale |
| `init_db.py` | Initialisation de la base (crée la table, insère les users) |
| `entrypoint.sh` | Script de démarrage du conteneur (attend PostgreSQL, lance init_db puis app) |
| `Dockerfile` | Image Docker de l'application Flask |
| `docker-compose.yml` | Définition de tous les services |
| `promtail-config.yml` | Configuration de l'agent de collecte de logs |
| `prometheus.yml` | Configuration de Prometheus |
| `audit.py` | Script de test d'injection SQL (Jour 2) |
| `audit_logs.py` | Script d'audit complet PostgreSQL + Docker (Jour 4) |

---

## Commandes Docker utiles

```bash
# Voir les logs d'un service
docker compose logs web
docker compose logs db
docker logs flask_app
docker logs postgres_db

# Entrer dans un conteneur
docker exec -it flask_app bash
docker exec -it postgres_db psql -U admin -d tp_j2

# Réinitialiser la base
docker exec -it flask_app python init_db.py

# Voir l'état de tous les conteneurs
docker compose ps
```

---

## Points de sécurité résiduelle à améliorer

- [ ] Externaliser les credentials dans un fichier `.env`
- [ ] Ajouter un rate limiting (Flask-Limiter, max 5 tentatives/min)
- [ ] Logger l'adresse IP source de chaque tentative
- [ ] Passer en HTTPS via Nginx + TLS
- [ ] Implémenter Flask-Login pour la gestion des sessions
- [ ] Ajouter les endpoints RGPD (droit à l'effacement)
- [ ] Désactiver `debug=True` en production
