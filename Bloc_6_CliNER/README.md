# Bloc 6 — Direction de Projet IA : CliNER (Clinical Trial Eligibility)

## 🎯 Objectif du Projet
**CliNER** (*Clinical Named Entity Recognition*) est une solution d'IA de **Reconnaissance d'Entités Nommées Médicales (Clinical NER)** et de traitement du langage naturel (NLP / Fine-Tuning LLM) dédiée à l'extraction automatique, la structuration et la validation des critères d'éligibilité des essais cliniques ([ClinicalTrials.gov](https://clinicaltrials.gov)). 

Elle résout le problème critique du recrutement des patients en recherche biomédicale, où **86 % des essais cliniques subissent des retards majeurs** dus à la complexité et au manque de structuration des critères d'inclusion et d'exclusion (souvent noyés dans des protocoles PDF de 50 à 100 pages).

---

## 🛠️ Stack Technique & Architecture IA
- **Moteur Clinical NER & Fine-Tuning LLM :** Extraction chirurgicale d'entités médicales complexes (Pathologies, Traitements/Molécules, Biomarqueurs, Mesures seuils, Temporalités) via **Qwen 2.5 7B** fine-tuné avec adaptateur **LoRA** (PEFT, 4-bit QLoRA) sur le corpus Gold Standard médical **CHIA** (1 000 études cliniques).
- **Embeddings Biomédicaux & Reranking :** **BioBERT v1.1** (768 dimensions) pour le chunking dense (512 tokens) et la sélection des Top-5 chunks (NER) / Top-15 chunks (Chatbot).
- **Data & Vector Store Managé :** **PostgreSQL** avec extension vectorielle **`pgvector`** et table de cache persistant `clinical_ner_cache` (hit 0,1s) hébergés sur **Supabase Cloud**, couplés à un stockage objet S3 (`clinical_pdfs`) avec zone de rejet.
- **Serving & Inférence Haute Performance :** **FastAPI** asynchrone propulsé par le moteur **vLLM** (débit ~75 tok/s) sur instance GPU dédiée **AWS EC2 g4dn.xlarge (NVIDIA T4)**.
- **Interface Praticien (Front-End) :** **Streamlit** multi-onglets (Recherche en direct, Table interactive avec cache session RAM, Dashboard visuel avec surlignage couleur des entités NER, Chatbot RAG sourcé) déployé sur **Render** (CI/CD GitHub Auto-Deploy).
- **Observabilité MLOps :** **MLflow Tracking & Model Registry** (suivi de la latence, traces applicatives RAG/NER, versions des adaptateurs LoRA).

---

## 🖼️ Architecture & Interface de Démonstration

### 1. Vue d'Ensemble du Pipeline Clinique
Pipeline de bout en bout intégrant l'ingestion ClinicalTrials, l'extraction d'entités par le LLM et la validation sémantique :

![Présentation du Projet CliNER](./assets/cliner_s3_img2.png)

### 2. Interface Utilisateur & Dashboard Médical
Interface praticien permettant de soumettre un protocole textuel ou un identifiant NCT pour obtenir l'extraction visuelle et la structuration JSON immédiate :

![Dashboard Médical CliNER](./app/assets/dashboard_medical.jpg)

### 3. Schéma Global de la Plateforme (Architecture & Flux de Données)
Organisation complète des flux de données entre l'interface Streamlit, le stockage Supabase Cloud, le serveur d'inférence GPU AWS EC2 (BioBERT + Qwen LoRA) et le suivi MLflow :

![Architecture Globale](./assets/cliner_s5_img3.jpg)

---

## 📂 Contenu du Répertoire
- `CliNER_presentation.pptx` : Support de présentation officiel (soutenance finale 10 min Demoday).
- `AIDE_MEMOIRE_ORAL_SLIDE_PAR_SLIDE_CLINER.pdf` : Fiche aide-mémoire slide par slide (format 1 page A4).
- `app/` : Application Web Streamlit avec surlignage d'entités médicales en direct.
- `api/` : API backend FastAPI exposant les endpoints d'inférence (NER & RAG).
- `scripts/` : Scripts d'inférence LoRA (`inference_qwen.py`) et d'ingestion/scraping en direct (`live_scraper.py`).
- `data/` : Échantillons annotés Chia Gold Standard pour la validation de performance.
- `Dockerfile` et `docker-compose.yml` : Configuration des conteneurs pour le déploiement de la solution.
- `assets/` : Schémas d'architecture et visuels de soutenance.
