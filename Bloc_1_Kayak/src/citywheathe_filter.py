# -*- coding: utf-8 -*-
import requests
import time
import pandas as pd
import uuid
import statistics
import datetime
import os
import sys

# --- CONFIGURATION API ---
# IMPORTANT : Définie via variable d'environnement ou fichier .env
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "VOTRE_CLE_OPENWEATHERMAP_ICI") 
OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/forecast"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {'User-Agent': 'KayakProject/1.0'} 

# --- CONFIGURATION FICHIERS ---
NOM_FICHIER_METEO = 'destinations_france_avec_meteo.csv'
NOM_FICHIER_TOP5 = 'top_5_destinations.csv' 

# Liste des 35 villes fournie par l'énoncé
VILLES_FRANCE = [
    "Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen", "Paris", "Amiens", 
    "Lille", "Strasbourg", "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim", 
    "Besancon", "Dijon", "Annecy", "Grenoble", "Lyon", "Gorges du Verdon", 
    "Bormes les Mimosas", "Cassis", "Marseille", "Aix en Provence", "Avignon", 
    "Uzes", "Nimes", "Aigues Mortes", "Saintes Maries de la mer", "Collioure", 
    "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne", "La Rochelle"
]
print(f"Nombre de villes à traiter : {len(VILLES_FRANCE)}")



# ÉTAPE 1 : Acquisition des Coordonnées GPS (Nominatim)

def get_gps_coordinates(city_name):
    """Obtient la latitude et la longitude pour un nom de ville (Nominatim)."""
    params = {
        'q': f"{city_name}, France", 
        'format': 'json',
        'limit': 1
    }
    
    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        if data:
            lat = float(data[0].get('lat'))
            lon = float(data[0].get('lon'))
            return lat, lon
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête Nominatim pour {city_name}: {e}")
    except (IndexError, TypeError):
        print(f"Coordonnées non trouvées pour {city_name}.")
        
    return None, None

def fetch_all_gps():
    """Récupère les GPS pour toutes les villes avec pause obligatoire."""
    city_gps_data = []
    print("\n--- 1. Acquisition GPS (Nominatim) ---")
    
    for city in VILLES_FRANCE:
        lat, lon = get_gps_coordinates(city)
        
        if lat and lon:
            city_gps_data.append({
                'city': city,
                'id': str(uuid.uuid4()), # ID unique pour la jointure
                'latitude': lat,
                'longitude': lon
            })
        
        # Pause obligatoire pour respecter les règles d'utilisation de Nominatim (1 requête/seconde max)
        time.sleep(1.5) 

    df_gps = pd.DataFrame(city_gps_data)
    print(f"Coordonnées GPS récupérées pour {len(df_gps)} villes.")
    return df_gps


#ÉTAPE 2 : Acquisition des Métriques Météo (OpenWeatherMap)

def fetch_weather_metrics(row):
    """
    Récupère les données météo d'OpenWeatherMap pour 5 jours (forecast)
    et calcule la Température Moyenne Max et la Médiane de Probabilité de Pluie (POP).
    """
    lat = row['latitude']
    lon = row['longitude']
    
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHERMAP_API_KEY,
        'units': 'metric',
        'lang': 'fr'
    }
    
    try:
        response = requests.get(OPENWEATHERMAP_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        forecast_list = data.get('list', [])
        daily_max_temps = {}
        daily_pops = {}

        for item in forecast_list:
            dt = item['dt']
            date_str = datetime.datetime.fromtimestamp(dt).strftime('%Y-%m-%d')
            
            temp_max = item['main'].get('temp_max', -float('inf'))
            pop = item.get('pop', 0)

            # Agrégation : Max de la température et de la POP par jour
            if date_str not in daily_max_temps or temp_max > daily_max_temps[date_str]:
                daily_max_temps[date_str] = temp_max
                
            if date_str not in daily_pops or pop > daily_pops[date_str]:
                 daily_pops[date_str] = pop

        temps_max_c = list(daily_max_temps.values())
        prob_precipitations = list(daily_pops.values())
        
        if not temps_max_c:
            return pd.Series([None, None])
            
        avg_temp = statistics.mean(temps_max_c)
        median_pop = statistics.median(prob_precipitations)
        
        time.sleep(0.5) # Pause
        return pd.Series([avg_temp, median_pop])

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"--- Attention : Erreur 401 pour {row['city']}. Clé API inactive ? ---")
        else:
            print(f"Erreur HTTP pour {row['city']} ({e.response.status_code}): {e}")
    except Exception as e:
        print(f"Erreur inconnue pour {row['city']}: {e}")
        
    time.sleep(0.5) 
    return pd.Series([None, None])

def fetch_all_weather(df_gps):
    """Applique la récupération météo au DataFrame GPS."""
    print("\n--- 2. Acquisition Météo (OpenWeatherMap) ---")
    
    df_metrics = df_gps.apply(fetch_weather_metrics, axis=1, result_type='expand')
    df_metrics.columns = ['avg_temp_c', 'median_pop']
    
    # Fusionner les nouvelles colonnes au DataFrame de base
    df_villes_final = pd.concat([df_gps, df_metrics], axis=1)
    
    return df_villes_final


# ÉTAPE 3 : Classement du Top 5 et Sauvegarde

def calculate_and_save_top_5(df_villes):
    """Nettoie, calcule le top 5 des destinations et sauvegarde les deux fichiers CSV."""
    
    # 1. Nettoyage et conversion des données
    df_villes['avg_temp_c'] = pd.to_numeric(df_villes['avg_temp_c'], errors='coerce')
    df_villes['median_pop'] = pd.to_numeric(df_villes['median_pop'], errors='coerce')

    df_villes_clean = df_villes.dropna(subset=['avg_temp_c', 'median_pop']).copy()
    
    if df_villes_clean.empty:
        print("\n--- ERREUR CRITIQUE --- Le DataFrame est vide après nettoyage.")
        return

    # 2. Détermination du TOP 5
    # Tri par température (décroissant) puis POP (croissant)
    df_top_5_villes = df_villes_clean.sort_values(
        by=['avg_temp_c', 'median_pop'], 
        ascending=[False, True]
    ).head(5)

    print("\n--- Top 5 des destinations selon les critères Météo ---")
    # ✅ CORRECTION: Utilisation de float_format pour forcer 4 chiffres après la virgule
    print(df_top_5_villes[['city', 'avg_temp_c', 'median_pop']].to_string(
        index=False, 
        float_format='%.4f'
    ))
    
    # 3. Sauvegarde des résultats
    
    # Sauvegarde du fichier complet
    df_villes.to_csv(NOM_FICHIER_METEO, index=False, encoding='utf-8')
    print(f"\nSUCCESS : DataFrame complet sauveguarde dans : {NOM_FICHIER_METEO}")
    
    # Sauvegarde du fichier Top 5 (utilisé par le scraper des hôtels)
    df_top_5_villes.to_csv(NOM_FICHIER_TOP5, index=False, encoding='utf-8')
    print(f"SUCCESS : Fichier Top 5 (filtre) sauveguarde dans : {NOM_FICHIER_TOP5}")



if __name__ == '__main__':
    # Étape 1 : Acquisition des GPS
    df_villes_gps = fetch_all_gps()
    
    # Vérification de sécurité
    if df_villes_gps.empty:
        print("\nERROR Arrêt du script : Aucune coordonnée GPS n'a pu être récupérée.")
        sys.exit(1)
        
    # Étape 2 : Acquisition de la Météo
    df_final = fetch_all_weather(df_villes_gps)
    
    # Étape 3 : Classement et Sauvegarde
    calculate_and_save_top_5(df_final)

    print("\n--- FIN DU SCRIPT D'ACQUISITION DES VILLES ---")