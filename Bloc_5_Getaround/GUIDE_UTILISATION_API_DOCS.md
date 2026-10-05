# Guide & Note d'Utilisation de l'API GetAround Pricing

**URL de production Swagger UI :** [https://elkristobal59-getaround-pricing-api.hf.space/docs](https://elkristobal59-getaround-pricing-api.hf.space/docs)  
**URL alternative ReDoc :** [https://elkristobal59-getaround-pricing-api.hf.space/redoc](https://elkristobal59-getaround-pricing-api.hf.space/redoc)  
**Espace Hugging Face Spaces :** [https://huggingface.co/spaces/Elkristobal59/getaround-pricing-api](https://huggingface.co/spaces/Elkristobal59/getaround-pricing-api)  
**Auteur :** Christopher Gilleron — Certification CDSD (RNCP 35288 - Bloc 5)

---

## 1. Présentation de la Documentation Interactive Swagger UI (`/docs`)

FastAPI génère automatiquement une interface interactive conforme au standard **OpenAPI 3.0** accessible directement sur l'endpoint `/docs`.

### Comment tester un endpoint en direct sans coder ?
1. Rendez-vous sur [https://elkristobal59-getaround-pricing-api.hf.space/docs](https://elkristobal59-getaround-pricing-api.hf.space/docs).
2. Cliquez sur l'endpoint souhaité (par exemple `POST /predict`).
3. Cliquez sur le bouton **"Try it out"** en haut à droite du bloc de l'endpoint.
4. L'interface pré-remplit un payload JSON d'exemple valide. Vous pouvez modifier les valeurs (ex: changer `mileage` à `50000` ou `engine_power` à `130`).
5. Cliquez sur le gros bouton bleu **"Execute"**.
6. L'interface affiche instantanément :
   - La commande `curl` générée.
   - L'URL de la requête appelée.
   - Le code HTTP de réponse (`200 OK`, `422 Validation Error`, etc.).
   - Le corps JSON de la réponse avec le prix prédit et la fourchette recommandée.

---

## 2. Cartographie Complète des Endpoints

| Méthode | Endpoint | Tag | Rôle & Description |
| :---: | :--- | :---: | :--- |
| `GET` | `/` | System | **Healthcheck & Architecture :** Vérifie le statut en ligne de l'API, confirme que le modèle de ML est chargé, identifie la source du modèle (MLflow Registry ou Cache Local Haute Disponibilité) et fournit les liens vers `/docs` et `/redoc`. |
| `GET` | `/info` | System | **Métadonnées & Catégories :** Retourne les performances du modèle ($R^2 = 0.729$, $\text{MAE} = 10.78\ €/\text{j}$) et la liste exhaustive des catégories supportées (28 marques, 4 carburants, 8 carrosseries, 10 couleurs). |
| `POST` | `/predict` | Inference | **Inférence Unitaire Universelle :** Accepte à la fois le format structuré Pydantic v2 (`CarFeatures`) et le format brut historique Jedha (`{"input": [[...]]}`). Renvoie le prix calculé, le prix arrondi et une fourchette recommandée ($\pm 11\ €$). |
| `POST` | `/predict/batch` | Inference | **Inférence par Lot :** Permet aux gestionnaires de flotte et loueurs professionnels d'estimer en un seul appel HTTP les prix d'un parc entier de véhicules (`BatchCarFeatures`). |
| `POST` | `/predict/legacy` | Inference | **Rétro-compatibilité stricte :** Accepte exclusivement le format historique liste de listes `{"input": [[...]]}` et retourne `{"prediction": [134]}`. |

---

## 3. Exemples Pratiques d'Appels & Payloads

### A. Endpoint `/predict` — Format Standard Pydantic v2 (Recommandé en Production)

#### Requête via Python (`requests`) :
```python
import requests

url = "https://elkristobal59-getaround-pricing-api.hf.space/predict"
payload = {
    "model_key": "Renault",
    "mileage": 50000,
    "engine_power": 110,
    "fuel": "diesel",
    "paint_color": "black",
    "car_type": "estate",
    "private_parking_available": True,
    "has_gps": True,
    "has_air_conditioning": True,
    "automatic_car": False,
    "has_getaround_connect": True,
    "has_speed_regulator": True,
    "winter_tires": False
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())
```

#### Réponse JSON reçue :
```json
{
  "prediction": [145.47],
  "predicted_price_per_day": 145.47,
  "rounded_price": 145,
  "currency": "EUR",
  "recommended_range": {
    "min_price": 134,
    "max_price": 156
  }
}
```

---

### B. Endpoint `/predict` — Format Jedha / Legacy (`{"input": [[...]]}`)

Ce format garantit la conformité stricte avec l'énoncé du projet Jedha :

#### Ordre des 13 variables dans la liste :
1. `model_key` (str, ex: `"Peugeot"`)
2. `mileage` (int, ex: `75000`)
3. `engine_power` (int, ex: `120`)
4. `fuel` (str, ex: `"diesel"`)
5. `paint_color` (str, ex: `"black"`)
6. `car_type` (str, ex: `"sedan"`)
7. `private_parking_available` (int 0/1, ex: `1`)
8. `has_gps` (int 0/1, ex: `1`)
9. `has_air_conditioning` (int 0/1, ex: `1`)
10. `automatic_car` (int 0/1, ex: `0`)
11. `has_getaround_connect` (int 0/1, ex: `1`)
12. `has_speed_regulator` (int 0/1, ex: `1`)
13. `winter_tires` (int 0/1, ex: `0`)

#### Requête en ligne de commande via cURL (Linux / macOS / Bash) :
```bash
curl -i -H "Content-Type: application/json" \
     -X POST \
     -d '{"input": [["Peugeot", 75000, 120, "diesel", "black", "sedan", 1, 1, 1, 0, 1, 1, 0]]}' \
     https://elkristobal59-getaround-pricing-api.hf.space/predict
```

#### Requête via Python (`requests`) :
```python
import requests

url = "https://elkristobal59-getaround-pricing-api.hf.space/predict"
payload = {
    "input": [
        ["Peugeot", 75000, 120, "diesel", "black", "sedan", 1, 1, 1, 0, 1, 1, 0]
    ]
}

response = requests.post(url, json=payload)
print(response.json())
```

#### Réponse JSON reçue :
```json
{
  "prediction": [133.52],
  "predicted_price_per_day": 133.52,
  "rounded_price": 134,
  "currency": "EUR",
  "recommended_range": {
    "min_price": 123,
    "max_price": 145
  }
}
```

---

### C. Endpoint `/predict/batch` — Flotte de Véhicules

#### Requête via Python :
```python
import requests

url = "https://elkristobal59-getaround-pricing-api.hf.space/predict/batch"
payload = {
    "cars": [
        {
            "model_key": "Citroën",
            "mileage": 140000,
            "engine_power": 100,
            "fuel": "diesel",
            "paint_color": "grey",
            "car_type": "estate",
            "private_parking_available": True,
            "has_gps": False,
            "has_air_conditioning": True,
            "automatic_car": False,
            "has_getaround_connect": False,
            "has_speed_regulator": False,
            "winter_tires": False
        },
        {
            "model_key": "BMW",
            "mileage": 30000,
            "engine_power": 190,
            "fuel": "petrol",
            "paint_color": "blue",
            "car_type": "suv",
            "private_parking_available": True,
            "has_gps": True,
            "has_air_conditioning": True,
            "automatic_car": True,
            "has_getaround_connect": True,
            "has_speed_regulator": True,
            "winter_tires": True
        }
    ]
}

response = requests.post(url, json=payload)
print(response.json())
```

---

## 4. Sens Métier & Interprétation des Réponses

1. **`predicted_price_per_day` :** Valeur brute issue du Random Forest Regressor entraîné sur les 4 843 annonces réelles.
2. **`rounded_price` :** Tarif suggéré arrondi à l'euro pour l'affichage utilisateur sur le site web Getaround.
3. **`recommended_range` ($\pm 11\ €$) :**
   - Basée directement sur la **MAE du modèle (10,78 €/jour)**.
   - Plutôt que d'imposer un tarif rigide qui braquerait le propriétaire, la plateforme propose une **fourchette de négociation** :
     * Borne basse (`min_price`) : Tarif agressif pour maximiser le taux de réservation en basse saison ou lors de la mise en ligne d'une nouvelle annonce.
     * Borne haute (`max_price`) : Tarif haute saison ou forte demande locale.

---

## 5. Robustesse MLOps & Gestion des Erreurs

- **Validation Pydantic v2 :** Si un type est invalide (ex: un kilométrage négatif ou un texte à la place d'un entier), l'API renvoie immédiatement un code **`HTTP 422 Unprocessable Entity`** détaillant le champ exact en erreur.
- **Gestion des valeurs inconnues (`handle_unknown='ignore'`) :** Si un utilisateur soumet une marque ou un carburant rare absent du jeu d'entraînement, le pipeline Scikit-Learn neutralise les colonnes OHE correspondantes sans crasher, calculant une prédiction basée sur la puissance et le kilométrage.
- **Haute Disponibilité (Zero-Downtime Fallback) :** L'API interroge le registry MLflow distant, et bascule instantanément sur son cache sérialisé local `model.joblib` en cas d'indisponibilité réseau, assurant 100 % d'uptime.
