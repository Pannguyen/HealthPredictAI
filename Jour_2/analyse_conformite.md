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

### Données potentiellement excessives

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

# 6. Première matrice des risques

| Risque | Gravité | Impact | Niveau |
|--------|---------|--------|--------|
| fuite de données | élevée | élevé | critique |
| accès non autorisé cloud | élevée | élevé | critique |
| transfert hors UE non conforme | élevée | moyen | important |
| dépendance fournisseur cloud | moyen | moyen | modéré |
| conservation excessive | moyen | faible | faible |

---

# 7. Conclusion

L’analyse met en évidence plusieurs points de vigilance concernant la conformité RGPD, les transferts internationaux et les risques cloud.

Les principales priorités sont :

- vérifier la localisation des données.
- documenter les traitements.
- renforcer les mesures de sécurité.
- encadrer juridiquement les transferts hors UE.
- réduire les risques liés au Cloud Act.