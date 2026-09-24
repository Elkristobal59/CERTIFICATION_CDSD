---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# ✈️ Plan Your Trip with Kayak — Data Engineering Pipeline & Cloud Architecture
## 🏆 Certification Data Science & Data Engineering (RNCP Niveau 6 - Bloc 1)
**Auteur :** Christopher Gilleron | Promotion AIFS / DSFS

---

## 📌 1. Contexte Métier & Objectif du Projet
**Kayak** est un moteur de recherche de voyages leader mondial appartenant à *Booking Holdings*.
Les études utilisateurs de l'équipe marketing ont révélé que **70% des utilisateurs** planifiant un voyage recherchent des informations enrichies sur leur destination (climat, ensoleillement, meilleurs hôtels).

### 🎯 Mission Data Engineering :
1. **Collecte & Géocodage :** Récupérer les coordonnées GPS des 35 plus belles villes de France via l'API *Nominatim (OpenStreetMap)*.
2. **Acquisition Météo :** Collecter les prévisions météorologiques sur 5 jours via l'API *OpenWeatherMap* et calculer un score d'ensoleillement.
3. **Web Scraping :** Extraire les données de 20 hôtels par ville pour le Top 5 des destinations les plus ensoleillées sur *Booking.com* (100 hôtels au total).
4. **Data Lake (AWS S3) :** Stocker les données brutes sur un bucket Cloud *Amazon S3* via `boto3`.
5. **Data Warehouse (PostgreSQL) :** Structurer, nettoyer et ingérer les données dans une base relationnelle managée *PostgreSQL* pour alimenter les équipes analytiques.


## 🏗️ 2. Architecture Globale du Pipeline ETL
```text
┌──────────────────────┐      ┌──────────────────────┐
│  Nominatim API (GPS) │      │ OpenWeatherMap API   │
└──────────┬───────────┘      └──────────┬───────────┘
           │                             │
           └──────────────┬──────────────┘
                          ▼
         ┌─────────────────────────────────┐
         │  Scoring Météo & Top 5 Villes   │
         └────────────────┬────────────────┘
                          ▼
         ┌─────────────────────────────────┐
         │  Web Scraping (Booking.com)     │ ➔ 100 Hôtels (GPS, Prix, Notes)
         └────────────────┬────────────────┘
                          ▼
         ┌─────────────────────────────────────────────────┐
         │   Data Lake (AWS S3 Bucket) : CSV Raw Storage   │
         └────────────────┬────────────────────────────────┘
                          ▼
         ┌─────────────────────────────────────────────────┐
         │ Data Warehouse (PostgreSQL) : Table Relationnelle│
         └────────────────┬────────────────────────────────┘
                          ▼
         ┌─────────────────────────────────────────────────┐
         │ Cartographies Interactives (Plotly / Folium)    │
         └─────────────────────────────────────────────────┘
```

```python
# Imports des bibliothèques nécessaires
import os
import sys
import pandas as pd
import numpy as np
import requests
import boto3
import psycopg2
import plotly.express as px
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
print('✅ Environnement Python et librairies initialisés avec succès.')
```

## 📍 3. Étape 1 : Géocodage des 35 Villes Françaises & Collecte Météo

```python
# Liste officielle des 35 villes de l'étude
CITIES = [
    'Mont Saint Michel', 'St Malo', 'Bayeux', 'Le Havre', 'Rouen', 'Paris', 'Amiens',
    'Lille', 'Strasbourg', 'Chateau du Haut Koenigsbourg', 'Colmar', 'Eguisheim',
    'Besancon', 'Dijon', 'Annecy', 'Grenoble', 'Lyon', 'Gorges du Verdon',
    'Bormes les Mimosas', 'Cassis', 'Marseille', 'Aix en Provence', 'Avignon',
    'Uzes', 'Nimes', 'Aigues Mortes', 'Saintes Maries de la mer', 'Collioure',
    'Carcassonne', 'Ariege', 'Toulouse', 'Montauban', 'Biarritz', 'Bayonne', 'La Rochelle'
]

# Chargement du jeu de données météo consolidé
df_meteo = pd.read_csv('destinations_france_avec_meteo.csv')
print(f'Nombre de villes traitées : {len(df_meteo)}')
df_meteo.head()
```

```python
# Sélection du Top 5 des meilleures destinations (Température la plus haute, pluie minimale)
df_top5 = pd.read_csv('top_5_destinations.csv')
print('🏆 TOP 5 DES DESTINATIONS RECOMMANDÉES PAR KAYAK :')
df_top5[['city', 'avg_temp_c', 'median_pop']]
```

## 🏨 4. Étape 2 : Dataset Scrapé sur Booking.com
Pour les 5 villes retenues, nous avons extrait **20 hôtels par ville**, avec les coordonnées GPS exactes, le prix moyen par nuit, la note de satisfaction et un descriptif.

```python
# Chargement du dataset consolidé des 100 hôtels
df_hotels = pd.read_csv('booking_hotels_v25_final.csv', sep=';')
print(f'Total d\'hôtels scrapés : {len(df_hotels)}')
print(f'Répartition par ville :\n{df_hotels["city"].value_counts()}')
df_hotels.head(3)
```

## 🗺️ 5. Étape 3 : Cartographies Interactives Plotly
Visualisation géospatiale des destinations et des hôtels sélectionnés.

```python
# Carte 1 : Top 5 Destinations Météo
top_5_cities_df = df_hotels.sort_values(by='avg_temp_c', ascending=False).drop_duplicates(subset=['city_id']).head(5)

fig1 = px.scatter_map(
    top_5_cities_df,
    lat='latitude_city',
    lon='longitude_city',
    hover_name='city',
    hover_data={'avg_temp_c': ':.1f', 'median_pop': ':.2f', 'latitude_city': False, 'longitude_city': False},
    color='avg_temp_c',
    size=top_5_cities_df['avg_temp_c'],
    size_max=35,
    color_continuous_scale=px.colors.sequential.Sunsetdark,
    zoom=5.2,
    center={'lat': 44.5, 'lon': 4.0},
    height=600,
    title='Top 5 des Meilleures Destinations en France selon la Météo (Kayak)'
)
fig1.update_layout(map_style='open-street-map')
fig1.show()
```

```python
# Carte 2 : Top 20 Hôtels les Mieux Notés
top_20_hotels = df_hotels.sort_values(by=['booking_score', 'average_price'], ascending=[False, True]).head(20)

fig2 = px.scatter_map(
    top_20_hotels,
    lat='latitude',
    lon='longitude',
    hover_name='hotel_name',
    hover_data={'city': True, 'booking_score': ':.1f', 'average_price': True, 'latitude': False, 'longitude': False},
    color='booking_score',
    color_continuous_scale=px.colors.sequential.Viridis,
    size=top_20_hotels['booking_score'],
    size_max=22,
    zoom=5.5,
    center={'lat': 44.0, 'lon': 4.5},
    height=600,
    title='Top 20 des Meilleurs Hôtels sélectionnés par Kayak (Booking.com)'
)
fig2.update_layout(map_style='open-street-map')
fig2.show()
```

## ☁️ 6. Étape 4 : Ingestion dans le Data Lake (Amazon S3)
Téléversement automatisé du dataset brut vers Amazon Web Services (S3).

```python
# Configuration S3
s3_bucket = os.getenv('S3_BUCKET_NAME', 'mlflow-artifacts-comcast-chris')
s3_key = os.getenv('S3_FILE_KEY', 'kayak/raw_data/booking_hotels_v25_final.csv')

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'eu-west-3')
)

s3_client.upload_file('booking_hotels_v25_final.csv', s3_bucket, s3_key)
print(f'✅ SUCCÈS S3 : Dataset téléversé dans s3://{s3_bucket}/{s3_key}')
```

## 🏛️ 7. Étape 5 : Ingestion & Requêtes Analytiques dans le Data Warehouse (PostgreSQL)
Structuration relationnelle et requêtes SQL d'audit.

```python
# Connexion à PostgreSQL et exécution des requêtes SQL analytiques
conn = psycopg2.connect(
    host=os.getenv('RDS_HOST'),
    port=int(os.getenv('RDS_PORT', 5432)),
    database=os.getenv('RDS_DBNAME'),
    user=os.getenv('RDS_USER'),
    password=os.getenv('RDS_PASSWORD'),
    sslmode=os.getenv('RDS_SSLMODE', 'require')
)

sql_query = '''
SELECT 
    city, 
    COUNT(*) as nb_hotels, 
    ROUND(AVG(booking_score), 2) as note_moyenne, 
    ROUND(AVG(average_price), 2) as prix_moyen_eur,
    ROUND(AVG(avg_temp_c), 1) as temp_meteo_c
FROM kayak_hotels_data
GROUP BY city
ORDER BY temp_meteo_c DESC, note_moyenne DESC;
'''

df_sql_stats = pd.read_sql(sql_query, conn)
conn.close()

print('📊 RÉSULTATS DES REQUÊTES SQL DEPUIS LE DATA WAREHOUSE POSTGRESQL :')
df_sql_stats
```

## 🏁 8. Conclusion & Valeur Métier
Ce pipeline MLOps / Data Engineering permet à **Kayak** de :
* Automatiser la veille météorologique sur les destinations touristiques françaises.
* Recommander en temps réel des hôtels de qualité supérieure (> 8/10) aux meilleurs tarifs.
* Centraliser le patrimoine de données dans un **Data Lake Cloud (S3)** et un **Data Warehouse managé (PostgreSQL)** sécurisé.
