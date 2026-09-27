# 🎓 Guide Officiel de Soutenance & Bilan d'Audit — Certification CDSD (RNCP 35288)

**Candidat :** Christopher GILLERON  
**Formation :** Fullstack Data Science & Engineering — Jedha Bootcamp  
**Date de l'épreuve orale :** **8 octobre 2026 (17h00 – 18h10)** — Durée totale : **1h10 (70 min)**  
**Dépôt officiel des livrables (règle des 48h) :** **Au plus tard le 6 octobre 2026 à 17h00** (Sécurisé au **5 octobre 23h59**)  
**Répertoire racine :** `d:\PROJETS JEDHA\CERTIFICATION_CDSD`

---

## 🧭 Sommaire
1. [Architecture Globale & Récapitulatif des 6 Blocs](#1-architecture-globale--récapitulatif-des-6-blocs)
2. [Applications, Streamlit & APIs à Ouvrir le Jour J](#2-applications-streamlit--apis-à-ouvrir-le-jour-j)
3. [Bilan d'Audit & Améliorations Apportées (Bloc par Bloc)](#3-bilan-daudit--améliorations-apportées-bloc-par-bloc)
4. [Déroulé Pas-à-Pas de l'Épreuve Orale (1h10) & Timing](#4-déroulé-pas-à-pas-de-lépreuve-orale-1h10--timing)
5. [Archives ZIP Pré-Packagées pour Julie LMS](#5-archives-zip-pré-packagées-pour-julie-lms)

---

## 1. Architecture Globale & Récapitulatif des 6 Blocs

| Bloc | Compétence RNCP 35288 | Projet Soutenu à l'Oral (Pitch) | Projet(s) Déposé(s) en Complément | Durée Oral | Support Slides | Métriques & Validations Clés |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **Bloc 1** | **Infrastructure de Gestion de Données** (Data Lake, ETL, SQL, RGPD) | 🎙️ **Kayak Trip Planner** | — | **10 min**<br>*(5m pitch + 5m Q&A)* | 8 slides | • Scraping 100 hôtels (20 par ville top 5)<br>• S3 Data Lake `kayak-trip-planner-chris`<br>• PostgreSQL Supabase `kayak_hotels_data` |
| **Bloc 2** | **Analyse Exploratoire & Inférentielle** (EDA, PySpark, Statistiques) | 🎙️ **Tinder Speed Dating** | 📦 **Steam Video Games** *(Big Data PySpark)* | **10 min**<br>*(5m pitch + 5m Q&A)* | 8 slides (Tinder)<br>7 slides (Steam) | • 551 participants, 8 378 dates (42% oui, 16.5% match)<br>• Physique : facteur n°1 réel ($r=0.49$)<br>• PySpark Steam : 36 cellules exécutées Databricks |
| **Bloc 3** | **Machine Learning Données Structurées** (Supervisé, Non-supervisé) | 🎙️ **Conversion Rate Challenge** | 📦 **Walmart Store Sales**<br>📦 **The North Face** *(TF-IDF)* | **10 min**<br>*(5m pitch + 5m Q&A)* | 8 slides (Conv)<br>6 slides (Walmart)<br>5 slides (North Face) | • 284k sessions, split stratifié 80/20<br>• Modèle Champion LogReg (seuil 0.45) : **F1 = 0.7762**<br>• Walmart : **$R^2 > 0.93$** (Ridge/Lasso) |
| **Bloc 4** | **Deep Learning Données Non-Structurées** (NLP, Séquentiel, Asymétrie) | 🎙️ **AT&T SMS Spam Detector** | — | **10 min**<br>*(5m pitch + 5m Q&A)* | 8 slides | • 5 572 SMS, Bi-LSTM + Embedding Keras<br>• **F1 = 0.946**, Recall Spam = **94.0 %**<br>• Application Streamlit avec jauge décisionnelle |
| **Bloc 5** | **Industrialisation & MLOps** (API REST, Docker, MLflow) | 🎙️ **Getaround Pricing & Delays** | — | **10 min**<br>*(5m pitch + 5m Q&A)* | 7 slides | • 21 310 locations retards, 4 843 annonces prix<br>• Random Forest : MAE 10.78 €/j, $R^2 = 0.729$<br>• API FastAPI + Dashboard Streamlit + Docker |
| **Bloc 6** | **Direction de Projet IA** (Cadrage, FinOps, LLM, RAG, RGPD) | 🎙️ **CliNER Clinical Trials** | — | **20 min**<br>*(10m pitch + 10m Q&A)* | 8 slides | • Qwen-2.5-7B LoRA (CHIA), BioBERT RAG<br>• **Précision 63.0 %** (+19 pts), 75 tok/s vLLM<br>• MLflow (port 5000), Docker, Terraform, Cache Supabase (82 études) |

---

## 2. Applications, Streamlit & APIs à Ouvrir le Jour J

> 💡 **Conseil d'organisation :** Ouvrez vos terminaux et lancez les services 15 minutes avant le début de l'épreuve. Chaque application utilise un port dédié pour éviter tout conflit.

```
       PORT 5000                  PORT 8000                  PORT 8501                  PORT 8502                  PORT 8503
 ┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
 │     MLflow UI     │      │   FastAPI Docs    │      │  AT&T SMS Filter  │      │ Getaround Portal  │      │  CliNER Medical   │
 │(Bloc 5 & Bloc 6)  │      │ (Bloc 5 Getaround)│      │ (Bloc 4 Streamlit)│      │ (Bloc 5 Streamlit)│      │ (Bloc 6 Streamlit)│
 └───────────────────┘      └───────────────────┘      └───────────────────┘      └───────────────────┘      └───────────────────┘
```

### 1. Bloc 4 — Détecteur SMS Spam AT&T (Streamlit)
* **Chemin :** `d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_4_ATT_Spam_Detector`
* **Commande PowerShell :**
  ```powershell
  cd "d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_4_ATT_Spam_Detector"
  C:\Users\maxpl\miniconda3\envs\jedha\python.exe -m streamlit run app.py --server.port 8501
  ```
* **URL Navigateur :** `http://localhost:8501`
* **Ce qu'il faut montrer en direct au jury :**
  - Saisir un SMS de test légitime (ex: *"Are you coming to the football match tonight?"*) $\rightarrow$ Vert (Ham, probabilité < 1%).
  - Saisir un SMS de phishing bancaire/smishing (ex: *"URGENT: Your account is suspended, call 09061701461 to claim your 1000 prize"*) $\rightarrow$ Rouge (Spam, probabilité > 99%).
  - Déplacer le curseur de seuil de décision (politique stricte 0.70 pour 0 faux positif vs politique équilibrée 0.25).

---

### 2. Bloc 5 — Industrialisation Getaround (FastAPI + Streamlit + MLflow)
* **Chemin :** `d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_5_Getaround`

#### A. Backend API REST FastAPI (Documentation Swagger) :
* **Commande PowerShell :**
  ```powershell
  cd "d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_5_Getaround"
  C:\Users\maxpl\miniconda3\envs\jedha\python.exe -m uvicorn src.api:app --reload --port 8000
  ```
* **URL Navigateur :** `http://localhost:8000/docs`
* **Ce qu'il faut montrer en direct :**
  - Cliquer sur `POST /predict` $\rightarrow$ `Try it out` $\rightarrow$ `Execute` $\rightarrow$ Réponse JSON instantanée avec prix estimé par jour.
  - Montrer la validation Pydantic v2 des schémas d'entrée.

#### B. Dashboard Décisionnel Streamlit :
* **Commande PowerShell :**
  ```powershell
  cd "d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_5_Getaround"
  C:\Users\maxpl\miniconda3\envs\jedha\python.exe -m streamlit run src/dashboard.py --server.port 8502
  ```
* **URL Navigateur :** `http://localhost:8502`
* **Ce qu'il faut montrer en direct :**
  - **Onglet Analyse Retards :** Ajuster le curseur de battement (60 min vs 120 min) pour visualiser le compromis entre part de retards neutralisés et chiffre d'affaires préservé.
  - **Onglet Estimation de Prix :** Ajuster les caractéristiques d'un véhicule (kilométrage, puissance, options) et observer la prédiction du modèle Random Forest.

#### C. Serveur de Traçabilité MLflow (Observabilité) :
* **Commande PowerShell :**
  ```powershell
  cd "d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_5_Getaround"
  C:\Users\maxpl\miniconda3\envs\jedha\python.exe -m mlflow ui --port 5000
  ```
* **URL Navigateur :** `http://localhost:5000`
* **Ce qu'il faut montrer en direct :**
  - Les runs enregistrés lors de l'entraînement (`getaround-pricing-experiment`), les hyperparamètres et métriques ($R^2$, MAE) et les artéfacts modèles.

---

### 3. Bloc 6 — CliNER Clinical Trial Intelligence (Streamlit)
* **Chemin :** `d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_6_CliNER`
* **Commande PowerShell :**
  ```powershell
  cd "d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_6_CliNER"
  C:\Users\maxpl\miniconda3\envs\jedha\python.exe -m streamlit run app/streamlit_app.py --server.port 8503
  ```
* **URL Navigateur :** `http://localhost:8503`
* **Ce qu'il faut montrer en direct au jury :**
  - **Bannière & KPIs :** F1-score 58.3%, Précision 63%, 75 tok/s, Qwen 7B LoRA (40 Mo).
  - **Recherche de cohorte :** Saisir une pathologie (ex: *"Hepatocellular Carcinoma"* ou *"Diabetes"*), filtrer par Phase ou Critères d'éligibilité (Plan A API gratuit, 0 GPU consommé).
  - **Extraction d'entités (NER) :** Sélectionner une étude (ex: `NCT03601897`) et lancer l'analyse. Grâce au fallback de cache persistant Supabase (82 études en base Cloud `clinical_ner_cache`), les entités médicales s'affichent instantanément (< 0,2s) même si l'instance GPU distante n'est pas allumée !
  - **Chat RAG :** Poser une question clinique en langage naturel sur le protocole via l'index vectoriel BioBERT.

---

### 4. Bloc 1 — Cartes Interactives Kayak (Folium)
* **Fichiers :**
  - `d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_1_Kayak\top_5_destinations_meteo.html`
  - `d:\PROJETS JEDHA\CERTIFICATION_CDSD\Bloc_1_Kayak\top_20_hotels_france.html`
* **Affichage :** Double-cliquer pour ouvrir directement dans Google Chrome ou Edge, ou les afficher à travers le notebook exécuté `Kayak_trip_planner.ipynb`.

---

## 3. Bilan d'Audit & Améliorations Apportées (Bloc par Bloc)

### 📌 Bloc 1 : Kayak Trip Planner
* **S3 Bucket :** Bucket actif vérifié `kayak-trip-planner-chris` sur AWS région `eu-west-3`. Fichiers présents : `booking_hotels.csv`, `destinations_france_meteo.csv`, `top_5_destinations.csv`.
* **PostgreSQL Cloud :** Table `kayak_hotels_data` active sur Supabase avec les 100 hôtels et coordonnées GPS.
* **Notebook :** `Kayak_trip_planner.ipynb` exécuté avec succès en **7,48 s**.

### 📌 Bloc 2 : Tinder & Steam
* **Tinder :** Résolution d'un bug bloquant de nom de fichier (`Speed+Dating+Data.csv` vs `Speed_dating_data.csv`). Notebook `Tinder_speed_dating.ipynb` exécuté avec succès en **5,87 s** (551 participants, 8 378 rendez-vous, physique facteur n°1 réel à $r=0.49$).
* **Steam :** Conformité avec l'exigence formelle Jedha (les sorties Databricks n'étant plus partageables par lien public). Intégration de `Steam_databricks_executed.ipynb` contenant **36 cellules avec toutes les sorties d'exécution réelles**, schémas Spark et agrégations, en plus des 3 graphiques haute résolution.

### 📌 Bloc 3 : Machine Learning (Conversion Rate, Walmart, North Face)
* **Conversion Rate :** Notebook `Conversion_rate_prediction.ipynb` exécuté avec succès en **112 s** (284k sessions, split stratifié, modèle champion seuil 0.45 : **F1 = 0.7762**, conformité stricte avec les 8 slides).
* **Walmart :** `Walmart_sales_prediction.ipynb` exécuté en **7,59 s** ($R^2 = 0.9388$ en validation, Ridge/Lasso).
* **North Face :** Correction du nom de fichier `sample-data.csv` $\rightarrow$ `sample_data.csv`. Exécution TF-IDF et similarité cosinus en **18,98 s**.

### 📌 Bloc 4 : Deep Learning (AT&T SMS Spam Detector)
* **Environnement Keras :** Exécution sous l'environnement `jedha` avec TensorFlow 2.21.0 en **47,72 s**.
* **Artéfacts créés :** Génération fraîche de `att_spam_model.keras` (4,1 Mo) et `tokenizer.pickle`.
* **Application :** Validation du bon fonctionnement de `app.py` avec inférence test validée à 99,27% sur un SMS de phishing.

### 📌 Bloc 5 : Industrialisation (Getaround)
* **Dépendances :** Installation de `openpyxl`. Exécution du notebook `Getaround_analysis.ipynb` en **10,02 s**.
* **MLflow & Entraînement :** Exécution de `src/train.py`, enregistrement de l'expérience dans MLflow, ré-entraînement du modèle de production Random Forest dans `models/model.joblib`.
* **Test API :** Inférence sub-milliseconde validée sur FastAPI.

### 📌 Bloc 6 : Direction de Projet IA (CliNER) — CADRAGE STRICT CDSD
* **Périmètre Authentique CDSD (AIFS01 — `stack_equipe`) :**
  - **Frontend & Orchestration :** Streamlit (`app/streamlit_app.py`) et backend FastAPI (`api/main.py`).
  - **Inférence IA :** Modèle **Qwen-2.5-7B-Instruct** fine-tuné sur CHIA en **QLoRA 4-bit** (adaptateur ultra-léger de 40 Mo au lieu de 14 Go) couplé au retriever biomédical **BioBERT**. Moteur **vLLM** assurant **75 tokens/seconde**.
  - **Base de Données & Vector Store :** PostgreSQL Cloud avec extension `pgvector` et stockage d'archives protocoles PDF sur **Supabase Cloud**.
  - **Observabilité :** Serveur **MLflow** pour le suivi des latences FastAPI, le monitoring des hyperparamètres LLM (température, max tokens) et l'historique de convergence de la loss du fine-tuning (1.66 $\rightarrow$ 0.84, token accuracy 85.7%).
  - **Infrastructure & FinOps :** Déploiement reproductible via **Docker** et **Terraform** (IaC pour le schéma Supabase pgvector), instance GPU **AWS EC2** (`g4dn.xlarge`), et table de cache persistant `clinical_ner_cache` (82 études pré-extraites garantissant un coût GPU nul pour 40% des requêtes).
* **Résilience FinOps dans l'Application Streamlit :**
  - Fallback automatique `_fetch_from_supabase_cache(nct_id)` : si le backend GPU distant n'est pas allumé, l'application bascule sur les 82 études de la base Supabase ou sur `data/chia_predictions.json`.
  - Résultat : **Zéro risque d'écran blanc ou de crash en direct devant le jury**, latence d'affichage de 0,2s.
* **Notebook Maître Exécuté (`CliNER_project_overview.ipynb`) :**
  - Exécuté avec succès en **3,28 s**, reprenant le cadrage métier (86% de retards de recrutement), la validation scientifique sur CHIA (Précision 63% vs 44%), la connexion live à Supabase et la simulation d'inférence structurée en JSON.
* **⚠️ Clarification Frontière CDSD (Niveau 6) vs Architecte IA (Niveau 7) :**
  - Le code CDSD ne contient **pas de CI/CD GitHub Actions**, **pas de Continuous Training (CT) avec distance de Wasserstein via Evidently AI**, et **pas de script Boto3 AWS EC2 Auto-Kill**.
  - Ces briques d'automatisation continue avancées appartiennent au programme **Architecte en Intelligence Artificielle (RNCP 41993 - Niveau 7)** développé dans `AIL-FT-02/cliner-mlops`.
  - Lors de la soutenance CDSD, vous présentez fidèlement votre projet Fullstack `stack_equipe` centré sur le modèle LoRA, l'observabilité MLflow, l'architecture hybride et l'application fonctionnelle.

---

## 4. Déroulé Pas-à-Pas de l'Épreuve Orale (1h10) & Timing

### Blocs 1 à 5 : Format 10 minutes chacun (5 min pitch + 5 min Q&A)

```
00:00 ─────────────────── 05:00 ─────────────────── 10:00
      PITCH CANDIDAT (5m)       QUESTIONS JURY (5m)
```

1. **Bloc 1 — Kayak (10 min) :**
   - *Pitch (5m) :* Problématique de centralisation de données météo et hôtelières. Architecture 3-tiers : Web Scraping Scrapy $\rightarrow$ S3 Data Lake $\rightarrow$ Entrepôt PostgreSQL Supabase $\rightarrow$ Restitution cartographique Folium. Respect du RGPD (données d'hôtels publiques, zero PII).
   - *Questions types du jury :* Comment gérez-vous le rate-limiting sur Booking ? *Réponse : Download delay, User-Agent rotation, respect des robots.txt.* Pourquoi S3 avant SQL ? *Réponse : Séparation du stockage brut (Data Lake immuable) et du stockage analytique typé (Data Warehouse).*

2. **Bloc 2 — Tinder (10 min) :**
   - *Pitch (5m) :* Décalage entre préférences déclarées et comportement réel. 551 participants, 8 378 dates. Normalisation des échelles (10 vs 100). Découverte clé : le physique est le facteur réel n°1 ($r=0.49$) alors que l'intelligence et la sincérité sont surévaluées dans le discours.
   - *Questions types du jury :* Et si l'on veut traiter 10 millions de profils ? *Réponse : Transition vers PySpark (présenter en 30 secondes le projet complémentaire Steam et ses Window Functions).*

3. **Bloc 3 — Conversion Rate (10 min) :**
   - *Pitch (5m) :* Problématique de déséquilibre de classes (3,23% convertis). Piège de l'Accuracy à 96,8%. Pipeline sans fuite avec ColumnTransformer. Modèle champion Régression Logistique avec seuil de décision abaissé à 0,45 : F1-score maximisé à **0,7762** (Rappel 71,8%, Précision 84,5%). Interprétabilité directe par les Odds Ratios (Allemagne $\times 35$, Pages vues $\times 12,5$).
   - *Questions types du jury :* Pourquoi privilégier le seuil à SMOTE ? *Réponse : SMOTE déforme les probabilités calibrées ; le seuil est transparent et directement pilotable selon les coûts métiers d'acquisition.*

4. **Bloc 4 — AT&T Spam Detector (10 min) :**
   - *Pitch (5m) :* Coût d'erreur fortement asymétrique (bloquer un 2FA bancaire est critique). Limite de la baseline TF-IDF (31 spams ratés). Modèle Deep Learning Bi-LSTM + Embedding Keras divisant par plus de 3 les menaces manquées (F1 = 0,946, Rappel = 94,0%). Démonstration en direct de l'app Streamlit avec jauge de seuil.
   - *Questions types du jury :* Pourquoi pas un Transformer type BERT ? *Réponse : Contrainte de latence télécom (< 5 ms par SMS) et possibilité d'export TensorFlow Lite sur smartphone (Edge AI privé).*

5. **Bloc 5 — Getaround (10 min) :**
   - *Pitch (5m) :* Double contrainte : 57,4% de retards mais médiane de 53 min. 218 litiges consécutifs à neutraliser. Compromis seuil 60 vs 120 min. Modèle de tarification Random Forest ($R^2 = 0.729$, MAE 10.78 €/j). Architecture MLOps : FastAPI, Dashboard décisionnel Streamlit, conteneurisation Docker et traçabilité MLflow.
   - *Questions types du jury :* Comment évitez-vous les conflits de dépendances ? *Réponse : Conteneurisation Docker multi-services orchestrée par docker-compose.*

---

### Bloc 6 : Format 20 minutes (10 min pitch + 10 min Q&A)

```
00:00 ───────────────────────────── 10:00 ───────────────────────────── 20:00
        PITCH FINAL CANDIDAT (10m)             QUESTIONS / DÉBAT JURY (10m)
```

* **Slide 1–2 :** Cadrage stratégique : 86% d'échecs de recrutement clinique, protocoles PDF de 100 pages, impact financier colossal pour la recherche médicale.
* **Slide 3–4 :** Solution MVP & Démo en direct de l'application Streamlit (recherche par maladie, filtres multicritères, affichage instantané des entités médicales).
* **Slide 5–6 :** Architecture et Benchmark NER sur le Gold Standard CHIA : Qwen-2.5-7B fine-tuné avec LoRA (**Précision 63,0% vs 44,0% pour Qwen brut**), serving haute performance vLLM à **75 tokens/seconde**.
* **Slide 7–8 :** Perspectives & Industrialisation MLOps (Périmètre CDSD) :
  - **Intégration en Laboratoire & Automatisation :** Déploiement chez le praticien on-premise, ingestion automatisée (CRON) pour alimenter la base vectorielle Supabase, garantie du secret médical et conformité RGPD (*Privacy by Design*).
  - **Observabilité & Suivi MLflow (Port 5000) :** Suivi temps réel des latences FastAPI et paramètres LLM, traçabilité des runs LoRA (convergence de la loss 1.66 $\rightarrow$ 0.84, accuracy 85.7%), zone de rejet pour isoler les PDF corrompus.
  - **FinOps & Infrastructure Cloud :** Provisioning déclaratif Terraform du schéma Supabase pgvector, conteneurisation Docker & serving sur instance GPU AWS EC2 (`g4dn.xlarge`), cache persistant `clinical_ner_cache` (82 études en base Cloud) servant 40% des requêtes en 0,2s à coût GPU nul.

---

## 5. Archives ZIP Pré-Packagées pour Julie LMS

Pour le dépôt obligatoire 48h avant l'épreuve sur la plateforme Julie LMS, 6 archives `.zip` propres, optimisées et purgées de tout fichier cache ou secret sont prêtes dans le dossier :
`d:\PROJETS JEDHA\CERTIFICATION_CDSD\LIVRABLES_ZIP`

| Nom du Fichier ZIP | Bloc Concerné | Taille | Contenu Inclus |
| :--- | :---: | :---: | :--- |
| **`Livrables_Bloc_1_Kayak.zip`** | Bloc 1 | 18,23 Mo | Notebook exécuté, scripts ETL Scrapy, cartes Folium HTML, données CSV, PPTX (8 slides) |
| **`Livrables_Bloc_2_Analyse_Exploratoire.zip`** | Bloc 2 | 6,87 Mo | Notebook Tinder exécuté, notebook Steam exécuté Databricks, CSVs, assets, PPTX (8 & 7 slides) |
| **`Livrables_Bloc_3_Machine_Learning.zip`** | Bloc 3 | 6,07 Mo | 3 notebooks exécutés (Conversion, Walmart, North Face), datasets, prédictions, PPTX (8, 6, 5 slides) |
| **`Livrables_Bloc_4_ATT_Spam_Detector.zip`** | Bloc 4 | 5,81 Mo | Notebook exécuté, `app.py`, modèle `att_spam_model.keras`, tokenizer, fiche révision, PPTX (8 slides) |
| **`Livrables_Bloc_5_Getaround.zip`** | Bloc 5 | 6,85 Mo | Notebook exécuté, `api.py`, `dashboard.py`, `train.py`, `model.joblib`, Dockerfiles, data, PPTX (7 slides) |
| **`Livrables_Bloc_6_CliNER.zip`** | Bloc 6 | 3,96 Mo | `CliNER_project_overview.ipynb`, `streamlit_app.py`, `api/main.py`, scripts d'évaluation, data CHIA, PPTX (8 slides) |

> 🔒 **Garantie Sécurité :** Aucun fichier `.env` ou clé AWS/Supabase n'est inclus dans ces archives (les clés sont gérées par variables d'environnement et ignorées par `.gitignore`).

---
*Document généré et certifié conforme pour la session CDSD du 8 octobre 2026.*
