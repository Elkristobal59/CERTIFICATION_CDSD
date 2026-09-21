# Bloc 4 — Deep Learning : AT&T SMS Spam Detector

## 🎯 Objectif du Projet
Concevoir et entraîner un modèle de Deep Learning pour la détection automatique de spams SMS afin de protéger les abonnés télécoms en temps réel.

## 🛠️ Stack Technique
- **Deep Learning :** TensorFlow / Keras, Tokenizer, Word Embeddings, Réseaux Récurrents (LSTM / GRU / Bidirectional RNN).
- **Évaluation :** Matrice de confusion, Courbe ROC-AUC, F1-Score sur classe minoritaire.
- **Application :** Dashboard interactif Streamlit pour tester la classification en direct.

## 📂 Contenu du Dossier
- `ATT_spam_detector.ipynb` : Notebook d'entraînement, comparaison architectures RNN/LSTM et évaluation.
- `ATT_spam_detector_presentation.pptx` : Support de présentation officiel (soutenance 5 min).
- `spam.csv` : Dataset SMS étiqueté (ham / spam).
- `app.py` : Application Streamlit de démonstration en direct.
- `tokenizer.pickle` : Tokenizer sérialisé pour le pré-traitement textuel.
