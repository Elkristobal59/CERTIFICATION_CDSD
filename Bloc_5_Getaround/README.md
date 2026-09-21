# Bloc 5 — Industrialisation & Déploiement : Getaround

## 🎯 Objectif du Projet
Deux volets majeurs pour optimiser la plateforme Getaround :
1. **Étude décisionnelle des retards :** Dimensionner le seuil optimal de battement entre locations successives et mesurer l'impact sur le chiffre d'affaires des propriétaires.
2. **Moteur de tarification en production :** Entraîner un modèle de prédiction du prix de location journalier, le servir via une API REST sécurisée et fournir un dashboard interactif.

## 🛠️ Stack Technique
- **API Backend :** FastAPI, Pydantic, Uvicorn, Swagger UI (`/docs`).
- **Dashboard Web :** Streamlit (analyse interactive de l'impact business des retards).
- **Modélisation & Suivi :** Scikit-Learn, Joblib, MLflow.
- **Conteneurisation :** Docker, Docker Compose (orchestration multi-services).

## 📂 Contenu du Dossier
- `Getaround_analysis.ipynb` : Notebook d'analyse exploratoire des retards et du pricing.
- `Getaround_presentation.pptx` : Support de présentation officiel (soutenance 5 min).
- `src/` : Scripts de l'API FastAPI (`api.py`), du dashboard Streamlit (`dashboard.py`) et d'entraînement (`train.py`).
- `models/` : Modèle de Machine Learning sérialisé (`model.joblib`).
- `data/` : Jeux de données historiques des retards et des tarifs.
- `docker/` et `docker-compose.yml` : Configuration des conteneurs pour le déploiement local ou cloud.
