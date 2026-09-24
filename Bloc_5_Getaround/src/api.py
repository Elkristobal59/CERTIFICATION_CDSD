"""
API FastAPI pour l'inférence en temps réel du modèle de tarification GetAround.
Projet : GetAround Pricing Optimization - Certification CDSD Bloc 5
Auteur : Christopher Gilleron

Endpoints :
- GET / : Statut du service, version et liens de documentation
- GET /info : Valeurs acceptées pour les variables catégorielles et métadonnées du modèle
- POST /predict : Prédiction unitaire typée avec Pydantic et fourchette recommandée
- POST /predict/batch : Prédiction par lot pour les gestionnaires de flotte
- POST /predict/legacy : Rétro-compatibilité avec le format de test générique {"input": [[...]]}
"""

import os
import joblib
import pandas as pd
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Initialisation de l'API avec métadonnées OpenAPI
app = FastAPI(
    title="GetAround Pricing API",
    description="""
API d'estimation dynamique des prix journaliers de location GetAround.

Fonctionnalités :
- Inférence temps réel via Pipeline Scikit-Learn sérialisée
- Validation stricte des données d'entrée avec Pydantic v2
- Estimation du prix central et d'une fourchette recommandée (±10% basé sur la MAE)
- Support des requêtes unitaires et par lot (batch)
- Documentation interactive Swagger UI & ReDoc
    """,
    version="1.0.0",
    contact={
        "name": "Christopher Gilleron",
        "url": "https://github.com/Elkristobal59/getaround-deployment-project"
    }
)

# Configuration CORS pour autoriser les requêtes depuis Streamlit ou des applications tierces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# CHARGEMENT DYNAMIQUE DU MODÈLE (MLOps Architecture)
# Priorité 1 : MLflow Model Registry (Production / Staging)
# Priorité 2 : AWS S3 Artifact Store
# Priorité 3 : Cache local résilient (Zero-Downtime Fallback)
# ---------------------------------------------------------------------------
MODEL_URI = os.getenv("MLFLOW_MODEL_URI", "models:/GetAround_Pricing_Model/Production")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", None)
LOCAL_FALLBACK_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "model.joblib")
if not os.path.exists(LOCAL_FALLBACK_PATH):
    LOCAL_FALLBACK_PATH = "models/model.joblib"

model = None
model_source = "unloaded"

def load_production_model():
    """Charge dynamiquement le modèle de production depuis MLflow ou bascule sur le cache local."""
    global model, model_source
    
    # 1. Tentative de chargement via MLflow Model Registry
    if MLFLOW_TRACKING_URI or os.getenv("USE_MLFLOW_REGISTRY", "false").lower() == "true":
        try:
            import mlflow.pyfunc
            if MLFLOW_TRACKING_URI:
                mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            print(f"[MLOps] Connexion au Model Registry MLflow ({MODEL_URI})...")
            model = mlflow.pyfunc.load_model(MODEL_URI)
            model_source = f"MLflow Model Registry ({MODEL_URI})"
            print(f"[MLOps SUCCESS] Modèle de production chargé depuis {model_source}")
            return
        except Exception as e_mlflow:
            print(f"[MLOps WARNING] Impossible de joindre le Model Registry MLflow : {e_mlflow}")
            print("[MLOps FALLBACK] Basculement vers le cache local de haute disponibilité...")

    # 2. Fallback de haute disponibilité (Zero-Downtime Local Cache)
    if os.path.exists(LOCAL_FALLBACK_PATH):
        try:
            model = joblib.load(LOCAL_FALLBACK_PATH)
            model_source = f"Local High-Availability Cache ({LOCAL_FALLBACK_PATH})"
            print(f"[API] Modèle chargé avec succès via {model_source}")
        except Exception as e_joblib:
            print(f"[API ERROR] Échec du chargement du cache local : {e_joblib}")
    else:
        print(f"[API CRITICAL] Aucun modèle disponible (ni MLflow, ni fichier local : {LOCAL_FALLBACK_PATH})")

load_production_model()


# --- SCHÉMAS PYDANTIC ---

class CarFeatures(BaseModel):
    model_key: str = Field(
        ..., 
        description="Marque du véhicule", 
        json_schema_extra={"example": "Peugeot"}
    )
    mileage: int = Field(
        ..., 
        ge=0, 
        le=1000000, 
        description="Kilométrage total au compteur", 
        json_schema_extra={"example": 75000}
    )
    engine_power: int = Field(
        ..., 
        ge=20, 
        le=1000, 
        description="Puissance moteur en chevaux (cv)", 
        json_schema_extra={"example": 120}
    )
    fuel: str = Field(
        ..., 
        description="Type de carburant (diesel, petrol, hybrid_petrol, electro)", 
        json_schema_extra={"example": "diesel"}
    )
    paint_color: str = Field(
        ..., 
        description="Couleur de carrosserie (black, grey, white, blue, silver, red, etc.)", 
        json_schema_extra={"example": "black"}
    )
    car_type: str = Field(
        ..., 
        description="Type de carrosserie (sedan, suv, estate, hatchback, convertible, coupe, subcompact, van)", 
        json_schema_extra={"example": "sedan"}
    )
    private_parking_available: bool = Field(
        True, 
        description="Disponibilité d'un parking privé pour restitution", 
        json_schema_extra={"example": True}
    )
    has_gps: bool = Field(
        True, 
        description="GPS intégré au véhicule", 
        json_schema_extra={"example": True}
    )
    has_air_conditioning: bool = Field(
        True, 
        description="Système de climatisation", 
        json_schema_extra={"example": True}
    )
    automatic_car: bool = Field(
        False, 
        description="Transmission automatique (True) ou manuelle (False)", 
        json_schema_extra={"example": False}
    )
    has_getaround_connect: bool = Field(
        True, 
        description="Boîtier Getaround Connect (déverrouillage smartphone sans remise de clé)", 
        json_schema_extra={"example": True}
    )
    has_speed_regulator: bool = Field(
        True, 
        description="Régulateur / Limiteur de vitesse", 
        json_schema_extra={"example": True}
    )
    winter_tires: bool = Field(
        False, 
        description="Équipé de pneus neige / hiver", 
        json_schema_extra={"example": False}
    )


class PricePrediction(BaseModel):
    predicted_price_per_day: float = Field(..., description="Prix optimal calculé par le modèle (€/jour)")
    rounded_price: int = Field(..., description="Prix recommandé arrondi à l'euro le plus proche")
    currency: str = Field("EUR", description="Devise de facturation")
    recommended_range: dict = Field(
        ..., 
        description="Fourchette de prix suggérée au propriétaire (marge de négociation basée sur la MAE de 11€)"
    )


class BatchCarFeatures(BaseModel):
    cars: List[CarFeatures]


class BatchPredictionResponse(BaseModel):
    total_cars: int
    predictions: List[PricePrediction]


class LegacyInput(BaseModel):
    input: list  # Format historique [[...]]


# --- ENDPOINTS ---

@app.get("/", tags=["System"])
def root():
    """Vérification de l'état de l'API, traçabilité MLOps et liens d'accès."""
    return {
        "service": "GetAround Pricing API",
        "status": "online",
        "version": "1.0.0",
        "model_loaded": model is not None,
        "model_source": model_source,
        "mlops_architecture": "MLflow Model Registry / S3 with High-Availability Local Fallback",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/info", tags=["System"])
def get_info():
    """Retourne la liste des catégories acceptées et les métriques du modèle."""
    return {
        "model_type": "RandomForestRegressor + ColumnTransformer Pipeline",
        "metrics": {
            "test_mae_eur": 10.78,
            "test_r2": 0.729,
            "training_samples": 3874,
            "test_samples": 969
        },
        "supported_brands": [
            "Alfa Romeo", "Audi", "BMW", "Citroën", "Ferrari", "Fiat", "Ford",
            "Honda", "KIA Motors", "Lamborghini", "Lexus", "Maserati", "Mazda",
            "Mercedes", "Mini", "Mitsubishi", "Nissan", "Opel", "PGO", "Peugeot",
            "Porsche", "Renault", "SEAT", "Subaru", "Suzuki", "Toyota", "Volkswagen", "Yamaha"
        ],
        "supported_fuels": ["diesel", "electro", "hybrid_petrol", "petrol"],
        "supported_car_types": ["convertible", "coupe", "estate", "hatchback", "sedan", "subcompact", "suv", "van"],
        "supported_colors": ["beige", "black", "blue", "brown", "green", "grey", "orange", "red", "silver", "white"]
    }


def _predict_dataframe(df: pd.DataFrame) -> List[PricePrediction]:
    """Helper interne de prédiction."""
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="Modèle de tarification non disponible sur le serveur. Veuillez réentraîner le modèle."
        )
    
    try:
        preds = model.predict(df)
        results = []
        for p in preds:
            p_float = float(p)
            rounded = int(round(p_float))
            results.append(
                PricePrediction(
                    predicted_price_per_day=round(p_float, 2),
                    rounded_price=rounded,
                    currency="EUR",
                    recommended_range={
                        "min_price": max(10, rounded - 11),
                        "max_price": rounded + 11
                    }
                )
            )
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'inférence : {str(e)}")


@app.post("/predict", response_model=PricePrediction, tags=["Inference"])
def predict_price(car: CarFeatures):
    """
    Estime le prix de location journalier recommandé pour un véhicule donné.
    Retourne le prix central ainsi qu'une fourchette haute et basse suggérée.
    """
    car_dict = car.model_dump()
    # Conversion booléens en entiers
    for k, v in car_dict.items():
        if isinstance(v, bool):
            car_dict[k] = int(v)
            
    df_single = pd.DataFrame([car_dict])
    predictions = _predict_dataframe(df_single)
    return predictions[0]


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Inference"])
def predict_batch(batch: BatchCarFeatures):
    """
    Estime en une seule requête les prix d'un ensemble de véhicules.
    Idéal pour les loueurs professionnels et gestionnaires de flotte.
    """
    cars_data = []
    for car in batch.cars:
        cd = car.model_dump()
        for k, v in cd.items():
            if isinstance(v, bool):
                cd[k] = int(v)
        cars_data.append(cd)
        
    df_batch = pd.DataFrame(cars_data)
    predictions = _predict_dataframe(df_batch)
    return BatchPredictionResponse(
        total_cars=len(predictions),
        predictions=predictions
    )


@app.post("/predict/legacy", tags=["Inference"])
def predict_legacy(data: LegacyInput):
    """
    Endpoint de rétro-compatibilité pour les appels au format liste brute.
    """
    columns = [
        'model_key', 'mileage', 'engine_power', 'fuel', 'paint_color', 
        'car_type', 'private_parking_available', 'has_gps', 
        'has_air_conditioning', 'automatic_car', 'has_getaround_connect', 
        'has_speed_regulator', 'winter_tires'
    ]
    df_input = pd.DataFrame(data.input, columns=columns)
    for col in columns[6:]:
        df_input[col] = df_input[col].astype(int)
        
    predictions = model.predict(df_input)
    return {"prediction": [round(float(p)) for p in predictions]}
