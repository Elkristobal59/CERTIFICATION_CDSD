# -*- coding: utf-8 -*-
"""
===============================================================================
PROJET KAYAK - BLOC 1 : VISUALISATIONS CARTOGRAPHIQUES INTERACTIVES
SCRIPT : GENERATION DES CARTES PLOTLY (preparation.py)
===============================================================================
"""

import os
import sys
import pandas as pd
import plotly.express as px
import numpy as np

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Configuration des fichiers
INPUT_CSV_FILE = 'booking_hotels_v25_final.csv'
OUTPUT_HTML_MAP_1 = 'top_5_destinations_map.html'
OUTPUT_HTML_MAP_2 = 'top_20_hotels_map.html'

print(f"[INFO] Demarrage de la generation des cartes a partir de {INPUT_CSV_FILE}...")

try:
    df = pd.read_csv(INPUT_CSV_FILE, sep=';', encoding='utf-8')
except FileNotFoundError:
    print(f"[ERREUR] Le fichier {INPUT_CSV_FILE} est introuvable.")
    sys.exit(1)
except Exception as e:
    print(f"[ERREUR] Lecture CSV: {e}")
    sys.exit(1)

# Formatage des colonnes numeriques
df['booking_score'] = pd.to_numeric(df['booking_score'], errors='coerce')
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df['avg_temp_c'] = pd.to_numeric(df['avg_temp_c'], errors='coerce')
df['median_pop'] = pd.to_numeric(df['median_pop'], errors='coerce')
df['average_price'] = pd.to_numeric(df['average_price'], errors='coerce')

# --- CARTE 1 : TOP 5 DESTINATIONS METEO ---
print("\n--- CARTE 1 : TOP 5 DESTINATIONS METEO ---")

top_5_cities_df = (
    df.sort_values(by='avg_temp_c', ascending=False)
    .drop_duplicates(subset=['city_id'])
    .head(5)
)

print("\nTop 5 des villes meteo :")
print(top_5_cities_df[['city', 'avg_temp_c', 'median_pop']].to_string(index=False))

fig1 = px.scatter_map(
    top_5_cities_df,
    lat="latitude_city",
    lon="longitude_city",
    hover_name="city",
    hover_data={'avg_temp_c': ':.1f', 'median_pop': ':.2f', 'latitude_city': False, 'longitude_city': False},
    color="avg_temp_c",
    size=top_5_cities_df['avg_temp_c'],
    size_max=35,
    color_continuous_scale=px.colors.sequential.Sunsetdark,
    zoom=5.2,
    center={"lat": 44.5, "lon": 4.0},
    height=650,
    title="Top 5 des Meilleures Destinations en France selon la Météo (Kayak)"
)

fig1.update_layout(map_style="open-street-map")
fig1.write_html(OUTPUT_HTML_MAP_1)
print(f"[SUCCESS] Carte 1 sauvegardee sous '{OUTPUT_HTML_MAP_1}'")

# --- CARTE 2 : TOP 20 HOTELS LES MIEUX NOTES ---
print("\n--- CARTE 2 : TOP 20 HOTELS LES MIEUX NOTES ---")

top_hotels_df = df.copy()
top_hotels_df.dropna(subset=['latitude', 'longitude'], inplace=True)
top_hotels_df.sort_values(by=['booking_score', 'average_price'], ascending=[False, True], inplace=True)
top_20_hotels = top_hotels_df.head(20)

print("\nTop 20 des hotels (Score Booking.com avec GPS) :")
print(top_20_hotels[['hotel_name', 'city', 'booking_score', 'average_price']].to_string(index=False))

fig2 = px.scatter_map(
    top_20_hotels,
    lat="latitude",
    lon="longitude",
    hover_name="hotel_name",
    hover_data={
        'city': True,
        'booking_score': ':.1f',
        'average_price': True,
        'latitude': False,
        'longitude': False
    },
    color="booking_score",
    color_continuous_scale=px.colors.sequential.Viridis,
    size=top_20_hotels['booking_score'],
    size_max=22,
    zoom=5.5,
    center={"lat": 44.0, "lon": 4.5},
    height=650,
    title="Top 20 des Meilleurs Hôtels sélectionnés par Kayak (Booking.com)"
)

fig2.update_layout(map_style="open-street-map")
fig2.write_html(OUTPUT_HTML_MAP_2)
print(f"[SUCCESS] Carte 2 sauvegardee sous '{OUTPUT_HTML_MAP_2}'")

print("\n--- GENERATION DES VISUALISATIONS TERMINEE ---")