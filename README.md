# Cartographie des flux de données — HealthPredict

## Schéma des flux de données

```mermaid
flowchart TD

    U[Utilisateur] -->|Questionnaire santé<br/>Nom, email, âge<br/>Symptômes, historique médical| F[Application Web Frontend]

    F -->|Transmission HTTPS<br/>Données personnelles<br/>Données sensibles<br/>Données techniques| API[API Backend]

    API -->|Validation / normalisation| DB[Base de données opérationnelle]

    DB -->|Export / conservation sécurisée| S3[Stockage chiffré AWS S3]

    S3 -->|Données pseudonymisées / chiffrées| PRE[Prétraitement / Feature engineering]

    PRE -->|Données préparées| ML[Modèle Machine Learning]

    ML -->|Score de risque maladie| API

    API -->|Résultat de prédiction| F

    F -->|Affichage du score| U

    API -->|Données agrégées / résultats| DASH[Dashboard interne]

    DASH -->|Consultation sécurisée| TEAM[Équipe interne]

    S3 -.->|Accès restreint / audit| DASH


