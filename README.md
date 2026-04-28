# Cartographie des flux de données — HealthPredict

## Schéma des flux de données

```mermaid
flowchart TD

    U[Utilisateur] -->|Saisie questionnaire santé<br/>Nom, email, âge<br/>Symptômes, historique médical| F[Application Web Frontend]

    F -->|Transmission HTTPS<br/>Données personnelles<br/>Données sensibles<br/>Données techniques| API[API Backend]

    API -->|Stockage des données| S3[AWS S3]

    API -->|Envoi données santé| ML[Modèle Machine Learning]

    ML -->|Score de risque| API

    API -->|Résultat| F

    F -->|Affichage| U

    API -->|Données| DASH[Dashboard interne]

    S3 -->|Accès données| DASH

    DASH -->|Accès équipes| TEAM[Équipe interne]