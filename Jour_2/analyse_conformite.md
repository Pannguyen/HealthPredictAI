# Analyser la conformité du système au regard du RGPD, des transferts de données hors UE et des risques liés au cloud.

## 1. Identification des traitements de données

L’entreprise réalise plusieurs traitements de données personnelles.

### Données collectées

- nom / prénom
- adresse email
- identifiant utilisateur
- mot de passe
- données de connexion
- journaux d’activité (logs)
- données clients / utilisateurs
- address
- numéro de téléphone

### Traitements réalisés

- authentification utilisateur
- gestion des comptes
- stockage des données applicatives
- sauvegarde et hébergement cloud
- supervision et journalisation
- support et maintenance

---

# 2. Analyse de conformité RGPD

## 2.1 Finalité des traitements

Le RGPD impose que les données soient collectées pour une finalité déterminée.

Finalités identifiées :

| Traitement | Finalité |
|------------|----------|
| Authentification | permettre la connexion des utilisateurs |
| Gestion des comptes | administrer les accès |
| Logs | sécurité et supervision |
| Hébergement cloud | disponibilité du service |

### Analyse

Les finalités apparaissent globalement cohérentes avec l’activité.

Point de vigilance :

- vérifier que toutes les finalités soient documentées.
- informer les utilisateurs via une politique de confidentialité.

---

## 2.2 Principe de minimisation

Le RGPD impose de ne collecter que les données strictement nécessaires.

### Données nécessaires

✓ email  
✓ identifiant utilisateur  
✓ mot de passe

### Données potentiellement excessive

⚠ logs trop détaillés  
⚠ conservation excessive  
⚠ collecte de données non utilisées

### Analyse

Le principe de minimisation doit être vérifié régulièrement.

---

## 2.3 Protection des données sensibles

Le RGPD impose une protection renforcée des données sensibles.

Exemples :

- données médicales
- données biométriques
- données financières
- opinions politiques
- données religieuses

### Mesures attendues

- chiffrement
- contrôle d’accès
- journalisation
- segmentation des droits
- sauvegardes sécurisées

### Risque identifié

Absence de chiffrement ou contrôle d’accès insuffisant.

---

# 3. Analyse des transferts de données hors UE

L’entreprise utilise un fournisseur cloud susceptible d’héberger ou traiter les données hors Union Européenne.

Exemples :

- AWS
- Microsoft Azure
- Google Cloud

### Risques identifiés

- hébergement hors UE
- sous-traitants internationaux
- accès depuis pays tiers

### Cadre juridique applicable

RGPD — Chapitre V.

Transfert autorisé uniquement avec garanties adéquates :

- décision d’adéquation
- clauses contractuelles types (SCC)
- mesures supplémentaires

### Analyse

L’entreprise doit vérifier :

- localisation réelle des données
- pays de traitement
- mécanismes juridiques utilisés

---

# 4. Risques liés au Cloud Act et aux fournisseurs cloud

Le Cloud Act américain peut permettre aux autorités US d’accéder à certaines données détenues par des entreprises américaines.

Fournisseurs concernés :

- Microsoft
- Google
- Amazon

### Risques juridiques

- accès gouvernemental extraterritorial
- incompatibilité potentielle avec RGPD
- perte de maîtrise des données

### Risques organisationnels

- dépendance fournisseur (vendor lock-in)
- faible maîtrise des sous-traitants
- difficulté d’audit

### Mesures de réduction du risque

- chiffrement fort
- gestion autonome des clés
- localisation UE
- audit fournisseur
- contractualisation renforcée

---

# 5. Non-conformités identifiées

| Domaine | Non-conformité |
|---------|----------------|
| Documentation | finalités insuffisamment documentées |
| Minimisation | collecte potentiellement excessive |
| Sécurité | chiffrement non démontré |
| Cloud | localisation des données non vérifiée |
| International | garanties de transfert non documentées |

---

# 6. Matrice des risques mise à jour (Plan d'Action de Remédiation)

Cette matrice évalue les risques en croisant la **Vraisemblance (V)** (liée aux non-conformités actuelles) et la **Gravité (G)** (impact potentiel), notées de 1 (Faible) à 4 (Critique). Elle intègre les mesures d'atténuation techniques et organisationnelles immédiates.

| Identifiant & Risque | Source / Cause (Non-conformité) | V (1-4) | G (1-4) | Niveau Initial | Mesures de Remédiation / Atténuation (Plan d'action) |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **R1 : Fuite ou violation de données** *(Exfiltration d'identifiants ou d'emails)* | Absence de chiffrement démontré des données au repos et vulnérabilités applicatives (ex: SQL Injection). | **4** | **4** | **Critique** | - Chiffrement AES-256 des bases de données.<br>- Utilisation stricte de requêtes préparées (correction du code).<br>- Hachage des mots de passe via `bcrypt` ou `Argon2`. |
| **R2 : Accès extraterritorial illégal (Cloud Act)** *(Saisie de données hors-UE)* | Utilisation d'un cloud américain (AWS, Azure, GCP) sans gestion autonome ou cloisonnement des clés de chiffrement. | **3** | **4** | **Critique** | - Implémentation du mécanisme *BYOK* (*Bring Your Own Key*) pour la gestion interne des clés de chiffrement.<br>- Évaluation d'une migration vers des alternatives d'hébergement européennes qualifiées SecNumCloud (ex: OVHcloud). |
| **R3 : Transfert hors-UE non conforme** *(Sanctions réglementaires CNIL)* | Absence de documentation et de vérification des clauses contractuelles ou de la localisation physique des serveurs. | **4** | **3** | **Important** | - Cartographie immédiate de la localisation géographique des serveurs et des flux de données de l'hébergeur.<br>- Signature des Clauses Contractuelles Types (SCC) de l'UE et complétion d'une TIA (*Transfer Impact Assessment*). |
| **R4 : Non-respect des droits des personnes** *(Réclamations utilisateurs)* | Finalités floues, manque de transparence et absence d'une politique de confidentialité accessible à l'utilisateur. | **3** | **2** | **Important** | - Rédaction, validation et publication d'une politique de confidentialité transparente.<br>- Mise en conformité des formulaires (opt-in clairs) et tenue d'un registre des traitements (Art. 30 RGPD). |
| **R5 : Rétention excessive des données** *(Augmentation de la surface d'attaque)* | Conservation indéfinie et non documentée des logs applicatifs (Docker, PostgreSQL) et des comptes inactifs. | **3** | **2** | **Modéré** | - Définition et configuration d'une politique de rétention automatique des logs Docker et PostgreSQL (limitation à 6 mois maximum).<br>- Processus automatique de purge ou d'anonymisation des comptes inactifs depuis 2 ans. |
| **R6 : Dépendance technologique (Vendor Lock-in)** *(Incapacité à migrer)* | Utilisation exclusive de briques logicielles et de services propriétaires intégrés d'un unique fournisseur Cloud. | **2** | **2** | **Faible** | - Conception de l'architecture basée exclusivement sur des technologies open-source, standardisées et entièrement conteneurisées (Docker, PostgreSQL, Grafana) pour garantir une portabilité totale. |

---

# 7. Conclusion

L’analyse met en évidence plusieurs points de vigilance concernant la conformité RGPD, les transferts internationaux et les risques cloud.

Les principales priorités sont désormais basées sur l'exécution du plan de remédiation :
- Appliquer les mesures de sécurité techniques (chiffrement, requêtes préparées, gestion autonome des clés).
- Documenter formellement les traitements (registre et politique de confidentialité).
- Encadrer juridiquement les transferts hors UE en exigeant des fournisseurs la localisation de nos données au sein de l'Union Européenne.
- Réduire l'exposition au Cloud Act et limiter la rétention des logs applicatifs.