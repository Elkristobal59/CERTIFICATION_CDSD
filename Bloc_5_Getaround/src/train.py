"""
Script d'entraînement et d'évaluation du modèle de tarification GetAround.
Projet : GetAround Pricing Optimization - Certification CDSD Bloc 5
Auteur : Christopher Gilleron

Ce script :
1. Charge les données de tarification (get_around_pricing_project.csv).
2. Construit une Pipeline Scikit-Learn robuste (ColumnTransformer + StandardScaler + OneHotEncoder).
3. Entraîne et compare une Baseline (Ridge) et un modèle avancé (RandomForestRegressor).
4. Calcule les métriques clés de régression : MAE, RMSE, R² et erreur relative médiane.
5. Extrait et affiche les variables les plus prédictives (Feature Importance).
6. Sauvegarde la Pipeline entraînée dans models/model.joblib.
7. Enregistre les métriques et artefacts dans MLflow pour la traçabilité MLOps.
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import joblib

# Fix Windows console UTF-8 output if possible
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False


def load_data(data_path: str):
    """Charge et nettoie les données de tarification."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Fichier de données introuvable : {data_path}")
    
    df = pd.read_csv(data_path, encoding='utf-8')
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    # Nettoyage et types
    binary_cols = [
        'private_parking_available', 'has_gps', 'has_air_conditioning',
        'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires'
    ]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)
            
    return df


def build_pipeline(regressor):
    """Construit la pipeline de préprocessing et régression."""
    numeric_features = ['mileage', 'engine_power']
    categorical_features = ['model_key', 'fuel', 'paint_color', 'car_type']
    binary_features = [
        'private_parking_available', 'has_gps', 'has_air_conditioning',
        'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires'
    ]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
            ('bin', 'passthrough', binary_features)
        ],
        remainder='drop'
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', regressor)
    ])
    
    return pipeline


def evaluate_model(name: str, pipeline, X_test, y_test):
    """Évalue les performances d'une pipeline sur le jeu de test."""
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    median_price = np.median(y_test)
    rel_error = (mae / median_price) * 100
    
    return {
        "model": name,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "rel_error_pct": rel_error,
        "predictions": y_pred
    }


def main():
    parser = argparse.ArgumentParser(description="GetAround Pricing Training Script")
    parser.add_argument("--data-path", type=str, default="data/get_around_pricing_project.csv", help="Chemin du dataset CSV")
    parser.add_argument("--output-model", type=str, default="models/model.joblib", help="Chemin de sauvegarde du modèle")
    parser.add_argument("--use-mlflow", action="store_true", default=True, help="Activer le tracking MLflow")
    args = parser.parse_args()

    print("=" * 70)
    print("[GETAROUND] PRICING OPTIMIZATION - ENTRAINEMENT MLOps")
    print("=" * 70)

    # 1. Chargement des données
    print(f"\n[DATA] Chargement des donnees depuis : {args.data_path}")
    df = load_data(args.data_path)
    print(f"   -> {df.shape[0]} annonces chargees avec {df.shape[1]} variables.")
    print(f"   -> Prix median : {df['rental_price_per_day'].median():.1f} EUR/jour (Moyenne : {df['rental_price_per_day'].mean():.1f} EUR/jour)")

    # 2. Séparation Features / Target & Train / Test
    X = df.drop(columns=['rental_price_per_day'])
    y = df['rental_price_per_day']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    print(f"   -> Train set : {len(X_train)} lignes | Test set : {len(X_test)} lignes (20% split).")

    # 3. Baseline : Ridge Regression
    print("\n[BASELINE] Entrainement Baseline (Regression Lineaire regularisee - Ridge)...")
    baseline_pipe = build_pipeline(Ridge(alpha=1.0))
    baseline_pipe.fit(X_train, y_train)
    baseline_metrics = evaluate_model("Baseline (Ridge)", baseline_pipe, X_test, y_test)

    # 4. Modèle de Production : Random Forest Regressor
    print("[PRODUCTION] Entrainement modele de production (Random Forest Regressor)...")
    rf_params = {
        'n_estimators': 120,
        'max_depth': 18,
        'min_samples_split': 4,
        'min_samples_leaf': 2,
        'random_state': 42,
        'n_jobs': -1
    }
    rf_pipe = build_pipeline(RandomForestRegressor(**rf_params))
    rf_pipe.fit(X_train, y_train)
    rf_metrics = evaluate_model("Random Forest Regressor", rf_pipe, X_test, y_test)

    # 5. Synthèse comparative
    print("\n[EVALUATION] RESULTATS COMPARATIFS SUR LE JEU DE TEST :")
    print("-" * 75)
    print(f"{'Modele':<26} | {'MAE (EUR/j)':<11} | {'RMSE (EUR/j)':<12} | {'R2':<8} | {'Erreur Rel. (%)':<15}")
    print("-" * 75)
    for m in [baseline_metrics, rf_metrics]:
        print(f"{m['model']:<26} | {m['mae']:<11.2f} | {m['rmse']:<12.2f} | {m['r2']:<8.3f} | {m['rel_error_pct']:<15.1f}")
    print("-" * 75)

    gain_mae = baseline_metrics['mae'] - rf_metrics['mae']
    gain_r2 = (rf_metrics['r2'] - baseline_metrics['r2']) * 100
    print(f"-> Gain apporte par Random Forest : -{gain_mae:.2f} EUR/jour d'erreur et +{gain_r2:.1f} pts de R2.")

    # 6. Feature Importance
    try:
        preprocessor = rf_pipe.named_steps['preprocessor']
        cat_encoder = preprocessor.named_transformers_['cat']
        cat_feature_names = cat_encoder.get_feature_names_out(['model_key', 'fuel', 'paint_color', 'car_type']).tolist()
        feature_names = ['mileage', 'engine_power'] + cat_feature_names + [
            'private_parking_available', 'has_gps', 'has_air_conditioning',
            'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires'
        ]
        importances = rf_pipe.named_steps['regressor'].feature_importances_
        feat_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
        feat_df = feat_df.sort_values(by='importance', ascending=False)

        print("\n[EXPLICABILITE] TOP 5 DES VARIABLES LES PLUS IMPORTANTES :")
        for idx, row in feat_df.head(5).iterrows():
            print(f"   * {row['feature']:<30} : {row['importance']*100:.1f} %")
    except Exception as e:
        print(f"   Note sur les features : {e}")

    # 7. Sauvegarde du modèle
    os.makedirs(os.path.dirname(args.output_model), exist_ok=True)
    joblib.dump(rf_pipe, args.output_model)
    print(f"\n[SAVE] Pipeline de production sauvegardee dans : {args.output_model}")

    # 8. Tracking MLflow
    if args.use_mlflow and MLFLOW_AVAILABLE:
        print("\n[MLFLOW] Enregistrement du run dans MLflow...")
        try:
            mlflow.set_experiment("GetAround_Pricing_Optimization")
            with mlflow.start_run(run_name="RandomForest_Production_Pipeline"):
                mlflow.log_params(rf_params)
                mlflow.log_metric("test_mae", rf_metrics['mae'])
                mlflow.log_metric("test_rmse", rf_metrics['rmse'])
                mlflow.log_metric("test_r2", rf_metrics['r2'])
                mlflow.log_metric("test_rel_error_pct", rf_metrics['rel_error_pct'])
                mlflow.sklearn.log_model(rf_pipe, artifact_path="model")
                print("   -> Modele, hyperparametres et metriques loggues dans MLflow avec succes.")
        except Exception as e:
            print(f"   [MLFLOW WARNING] : {e}")
    else:
        print("\n[INFO] MLflow desactive ou non disponible.")

    print("\n[SUCCESS] Entrainement termine avec succes !")


if __name__ == "__main__":
    main()
