# Bloc 1 — Infrastructure de Données : Kayak Trip Planner

## 🎯 Objectif du Projet
Collecter, transformer et stocker des données météorologiques et hôtelières sur 35 villes de France afin d'aider les utilisateurs à planifier leurs vacances vers les destinations les plus ensoleillées au meilleur prix.

## 🛠️ Stack Technique
- **Scraping & API :** Scrapy, BeautifulSoup, OpenWeatherMap API (coordonnées GPS et prévisions météo).
- **Data Engineering & Cloud :** Python, Pandas, AWS S3 (Data Lake), AWS RDS PostgreSQL (Data Warehouse), Boto3, SQLAlchemy.
- **Visualisation Cartographique :** Plotly, Folium (cartes interactives des meilleures destinations).

## 📂 Contenu du Dossier
- `Kayak_trip_planner.ipynb` : Notebook complet d'exploration, appel API météo, calcul des scores et cartographie.
- `Kayak_presentation.pptx` : Support de présentation officiel (soutenance 5 min).
- `src/` : Scripts de scraping Booking.com, filtrage météo et ingestion AWS S3 / PostgreSQL.
- `data/` : Datasets nettoyés des hôtels et des prévisions météo.
- `maps/` : Cartes interactives HTML (`top_5_destinations_map.html`, `top_20_hotels_map.html`).
