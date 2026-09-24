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
- `models/` : Cache local haute disponibilité (`model.joblib`) pour exécution autonome hors-ligne (*Zero-Downtime Fallback*). En production, l'API se connecte dynamiquement au **Model Registry MLflow** / S3 Artifact Store.
- `data/` : Jeux de données historiques des retards et des tarifs.
- `docker/` et `docker-compose.yml` : Configuration des conteneurs pour le déploiement local ou cloud.

## 🌐 Déploiements en Ligne (Hugging Face Spaces)
Les services sont conteneurisés et déployés en production sur l'infrastructure cloud Hugging Face :
- 📊 **Dashboard Décisionnel (Streamlit) :** [https://huggingface.co/spaces/Elkristobal59/getaround-analysis-dashboard](https://huggingface.co/spaces/Elkristobal59/getaround-analysis-dashboard)
- ⚡ **API Inférence & Documentation Swagger UI :** [https://elkristobal59-getaround-pricing-api.hf.space/docs](https://elkristobal59-getaround-pricing-api.hf.space/docs)
  *(Espace Hugging Face de l'API : [Elkristobal59/getaround-pricing-api](https://huggingface.co/spaces/Elkristobal59/getaround-pricing-api))*

### 🔌 Endpoints de l'API en Production
| Méthode | Endpoint | Description |
| :---: | :--- | :--- |
| `GET` | `/` | Healthcheck, statut du service et traçabilité de l'architecture MLOps |
| `GET` | `/info` | Liste des marques/catégories acceptées et métriques de validation ($R^2$, $\text{MAE}$) |
| `POST` | `/predict` | Inférence unitaire universelle (schémas Pydantic v2 + format legacy) |
| `POST` | `/predict/batch` | Inférence groupée pour gestionnaires de flotte |
| `GET` | `/docs` | Documentation interactive Swagger UI avec console de test intégrée |

## 🚀 Architecture de Déploiement MLOps (Production-Ready)
L'API d'inférence FastAPI (`src/api.py`) est conçue selon les standards industriels MLOps modernes :
1. **Model Registry Centralisé (MLflow) :** Lors de l'entraînement (`src/train.py`), le pipeline de régression Random Forest est loggué et versionné dans MLflow avec ses hyperparamètres et métriques ($R^2 = 0.73$, $\text{MAE} = 10.8\ €$).
2. **Chargement Dynamique à Chaud :** Au boot, l'API interroge la variable `MLFLOW_MODEL_URI` (par défaut `models:/GetAround_Pricing_Model/Production`) pour charger dynamiquement la dernière version validée sans nécessiter de reconstruction de l'image Docker (*Zero-Rebuild Deployment*).
3. **Résilience & Haute Disponibilité :** Si le serveur MLflow distant est indisponible, l'API bascule automatiquement et de manière transparente sur le cache local (`models/model.joblib`), garantissant 100% d'uptime (*Zero-Downtime Fallback*).

