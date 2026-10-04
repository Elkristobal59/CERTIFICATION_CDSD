# Bloc 2 — Analyse du Marché Steam Video Games avec PySpark (Databricks)

## 🎯 Objectif Métier & Contexte
Dans le cadre d'une étude de marché pour orienter la conception, le pricing et le positionnement du prochain jeu phare d'**Ubisoft**, ce projet explore et quantifie à l'échelle Big Data l'intégralité du catalogue de la plateforme **Steam** (55 691 jeux vidéo uniques) grâce à **Apache Spark (PySpark)** sur cluster managé **Databricks** :
- **Évolution temporelle :** Mesure de la croissance des sorties (1997–2022) et quantification de l'impact de la crise sanitaire COVID-19.
- **Modèles économiques :** Arbitrage Free-to-Play vs Jeux payants, segmentation tarifaire et élasticité des soldes.
- **Paysage concurrentiel :** Benchmark du Top 10 des éditeurs mondiaux et positionnement d'Ubisoft.
- **Genres & Qualité :** Identification des genres leaders, calcul des proxys de chiffre d'affaires et seuils critiques de satisfaction joueur.
- **Écosystème technique :** Taux de couverture multi-OS (Windows, MacOS, Linux / Steam Deck) et localisation multilingue.

---

## ⚠️ Note sur la Publication Databricks & Livrables Officiels
> **Consigne officielle Jedha :** *« La publication n'étant plus disponible sur Databricks, il est demandé de réaliser des captures d'écran de tes sorties de cellules de code. »*
>
> **Livrables fournis dans ce dépôt :**
> 1. `Steam_databricks_executed.html` : **Rendu complet interactif exporté depuis le cluster Databricks**, contenant l'intégralité du code PySpark, des plans d'exécution Catalyst et des 26 visualisations graphiques générées via l'outil de dashboarding intégré `display()`.
> 2. `Steam_databricks_executed.ipynb` : Notebook Jupyter source contenant les cellules PySpark exécutées et leurs sorties sérialisées.
> 3. `Steam_presentation.pptx` : Présentation exécutive officielle calibrée à 8 slides (format soutenance 5 minutes) intégrant les graphiques haute résolution issus de Databricks.

---

## 🛠️ Stack Technique
- **Traitement Distribué & Big Data :** Apache Spark 3.x (PySpark), Spark SQL, Catalyst Optimizer, Window Functions, `explode_outer()`.
- **Plateforme & Cluster :** Databricks Cloud Environment.
- **Stockage Cloud :** AWS S3 (Dump JSON semi-structuré multi-niveaux `s3://full-stack-bigdata-datasets/Big_Data/Project_Steam/steam_game_output.json`).
- **Data Visualisation :** Databricks Built-in Visualization Engine (`display()`) & Matplotlib/Seaborn (thème sombre exécutif).

---

## 📊 Principaux Résultats & Chiffres Clés (Source : Cluster Databricks)

| Axe d'Analyse | Métrique Clé | Enseignement Stratégique pour Ubisoft |
| :--- | :--- | :--- |
| **Volume Global** | **55 691 jeux analysés** | Catalogue mondial consolidé après aplatissement du schéma JSON struct. |
| **Accélération COVID-19** | **8 823 sorties en 2021** (+26.6% vs 2019) | **30.8% du catalogue** publié en seulement 24 mois (2020–2021). Saturation de l'attention nécessitant un marketing Day One puissant. |
| **Monétisation** | **14.0% Gratuit (F2P) / 86.0% Payant** | Prix moyen catalogue : **7.73 €** (médiane : 4.99 €). 80% des jeux payants sous 15 €. |
| **Positionnement Ubisoft** | **128 jeux au catalogue** | Classé dans le **Top 10 mondial des éditeurs**, au coude-à-coude exact avec Electronic Arts (128). |
| **Titre Phare Ubisoft** | *Rainbow Six Siege* : **1.09 M d'avis** (86.8% positif) | Top 5 mondial de tous les temps. Modèle Live-Ops amorti sur le long terme. |
| **Genre le Plus Lucratif** | **Action : 1.05 Milliard d'€** (proxy CA) | 1er contributeur de revenus, suivi de l'Aventure (678 M€) et des RPG (492 M€). |
| **Panier Moyen Maximal** | **RPG : 9.04 €** prix moyen unitaire | Rentabilité unitaire 2.5 fois supérieure aux jeux indépendants. Recommandation : cibler un Action-RPG hybride à 29.99 €. |
| **Couverture Multi-OS** | **Windows 99.97% \| MacOS 22.9% \| Linux 15.2%** | Boom de Linux porté par le **Steam Deck** (+30% de ventes sans coût de portage grâce à Proton). |
| **Localisation** | **Anglais (99.0%), Allemand (25.2%), Chinois (24.5%)** | Le Chinois Simplifié est le 1er bassin d'expansion hors Occident. Doublage et sous-titrage obligatoires. |

---

## 📂 Contenu du Répertoire
- `Steam_databricks_executed.html` : **Rapport exécuté complet exporté depuis Databricks** (code + sorties graphiques intégrées).
- `Steam_databricks_executed.ipynb` : Notebook PySpark complet exécuté sur cluster.
- `Steam_presentation.pptx` : Support de soutenance 8 slides avec captures et graphiques Databricks.
- `assets/` : Graphiques décisionnels haute résolution (Sorties & COVID, Pricing, Revenus & Multi-OS).
