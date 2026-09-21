# Bloc 6 — Direction de Projet IA : CliNER (Clinical Trial Eligibility)

## 🎯 Objectif du Projet
CliNER est une plateforme d'IA médicale dédiée à l'extraction et à l'analyse automatique des critères d'éligibilité des essais cliniques (ClinicalTrials.gov) pour accélérer le recrutement des patients et réduire le taux d'échec des études cliniques.

## 🛠️ Stack Technique
- **Fine-Tuning LLM & NER :** Qwen-2.5-7B fine-tuné avec LoRA (PEFT, Hugging Face, Chia Corpus) pour l'extraction d'entités nommées cliniques (Inclusion / Exclusion, Pathologies, Biomarqueurs).
- **RAG & Recherche Sémantique :** BioBERT Embeddings + Supabase / PostgreSQL pgvector.
- **Architecture de Production :** FastAPI (inférence asynchrone), Streamlit (interface utilisateur interactive), Docker Compose.

## 📂 Contenu du Dossier
- `CliNER_presentation.pptx` : Support de présentation officiel (soutenance 10 min Demoday).
- `app/` : Application Web interactive Streamlit (saisie de protocoles, surlignage NER en direct).
- `api/` : API REST FastAPI connectée aux modèles d'inférence.
- `scripts/` : Scripts de démonstration d'inférence Qwen (`inference_qwen.py`), d'évaluation (`evaluate_ner_brateval.py`) et de scraping en direct.
- `data/` : Échantillons de données annotées (Chia Gold Standard) pour tests rapides.
- `Dockerfile` et `docker-compose.yml` : Fichiers d'orchestration pour le déploiement complet.
