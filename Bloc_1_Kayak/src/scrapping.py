# -*- coding: utf-8 -*-

import pandas as pd
import os
import time
import re
from csv import QUOTE_ALL
from playwright.sync_api import sync_playwright
import numpy as np 
from datetime import datetime, timedelta 
import sys

# --- CONFIGURATION ---
INPUT_CSV_FILE = 'top_5_destinations.csv'
OUTPUT_CSV_FILE = 'booking_hotels_v25_final.csv' 

COLUMNS_ORDER = [
    'city_id', 'city', 'latitude_city', 'longitude_city', 
    'avg_temp_c', 'median_pop',
    'hotel_name', 'hotel_description', 'booking_score', 
    'average_price', 'latitude', 'longitude'
]

TARGET_HOTELS_PER_CITY = 20 

# --- SÉLECTEURS STABLES ---
USER_AGENT_STRING = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
HOTEL_CONTAINER_SELECTOR = 'div[data-testid="property-card"]'
PRICE_TESTID_SELECTOR = '[data-testid="price-and-discounted-price"]' 

def print_console(msg):
    print(f"{time.strftime('%H:%M:%S')} - {msg}")

def load_cities():
    date_actuelle = datetime.now()
    date_arrivee = date_actuelle + timedelta(days=7)
    date_depart = date_arrivee + timedelta(days=2)
    print_console(f"Dates : {date_arrivee.strftime('%Y-%m-%d')} au {date_depart.strftime('%Y-%m-%d')}")
    try:
        try: df = pd.read_csv(INPUT_CSV_FILE, sep=',', encoding='utf-8')
        except: df = pd.read_csv(INPUT_CSV_FILE, sep=';', encoding='utf-8')
        df.rename(columns={'latitude': 'latitude_city', 'longitude': 'longitude_city'}, inplace=True)
        df['start_url'] = df['city'].apply(lambda x: f"https://www.booking.com/searchresults.fr.html?ss={x}&checkin={date_arrivee.strftime('%Y-%m-%d')}&checkout={date_depart.strftime('%Y-%m-%d')}&group_adults=2&no_rooms=1&sb_travel_purpose=leisure")
        return df
    except Exception as e:
        print_console(f"Erreur CSV: {e}"); return None

def extract_basic_info(card, city_row):
    try:
        title_el = card.query_selector('[data-testid="title"]')
        name = title_el.inner_text().split('\n')[0].replace("Une nouvelle fenêtre va s'ouvrir", "").strip()
        url = card.query_selector('a[data-testid="title-link"]').get_attribute('href').split('?')[0]
        
        price = 'N/A'
        price_el = card.query_selector(PRICE_TESTID_SELECTOR)
        if price_el:
            m = re.search(r'€\s*(\d[\s\d]*\d)', price_el.inner_text())
            price = m.group(1).replace(' ', '') if m else re.sub(r'[^\d]', '', price_el.inner_text()).strip()

        score = 'N/A'
        score_el = card.query_selector('[data-testid="review-score"] div:first-child')
        if score_el:
            m = re.search(r'(\d+([.,]\d+)?)', score_el.inner_text())
            if m: score = m.group(1).replace(',', '.')

        lat, lon = 'N/A', 'N/A'
        for attr in ['data-coords', 'data-latitude', 'data-longitude']:
            val = card.get_attribute(attr)
            if val:
                if ',' in val: lat, lon = val.split(',')
                else:
                    if attr == 'data-latitude': lat = val
                    if attr == 'data-longitude': lon = val

        return {'city_id': city_row['id'], 'city': city_row['city'], 'hotel_name': name, 'hotel_url': url, 'booking_score': score, 'average_price': price, 'latitude': lat, 'longitude': lon}
    except: return None

def deep_scrape_info(page, url):
    lat, lon, desc = 'N/A', 'N/A', 'N/A'
    try:
        page.goto(url, timeout=45000, wait_until="domcontentloaded")
        time.sleep(1)
        # Description
        for sel in ['p[data-testid="property-description"]', '#property_description_content', '.hp_desc_main_content']:
            el = page.query_selector(sel)
            if el:
                txt = el.inner_text().strip()
                if len(txt) > 50: desc = txt[:500].replace('\n', ' '); break
        # GPS
        m_lat = page.query_selector('meta[property="booking_com:location:latitude"]')
        m_lon = page.query_selector('meta[property="booking_com:location:longitude"]')
        if m_lat and m_lon: lat, lon = m_lat.get_attribute('content'), m_lon.get_attribute('content')
        else:
            j_lat = page.evaluate('() => window.booking ? window.booking.env.b_map_center_latitude : null')
            j_lon = page.evaluate('() => window.booking ? window.booking.env.b_map_center_longitude : null')
            if j_lat and j_lon: lat, lon = str(j_lat), str(j_lon)
    except: pass
    return lat, lon, desc

def run_scraper():
    df_villes = load_cities()
    if df_villes is None: return

    final_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=USER_AGENT_STRING)
        
        page_search = context.new_page()
        page_detail = context.new_page() # DEUXIÈME ONGLET POUR LE DÉTAIL

        for _, city_row in df_villes.iterrows():
            print_console(f"\n--- Ville : {city_row['city']} ---")
            valid_hotels = []
            
            try:
                page_search.goto(city_row['start_url'], timeout=60000)
                try: page_search.click('#onetrust-accept-btn-handler', timeout=3000)
                except: pass
                
                # Scroll
                for _ in range(3): page_search.mouse.wheel(0, 4000); time.sleep(1)
                
                cards = page_search.query_selector_all(HOTEL_CONTAINER_SELECTOR)
                print_console(f"Recherche parmi {len(cards)} hôtels...")

                for card in cards:
                    if len(valid_hotels) >= TARGET_HOTELS_PER_CITY: break
                    
                    basic = extract_basic_info(card, city_row)
                    if not basic: continue
                    
                    # On utilise l'autre onglet pour ne pas perdre la recherche
                    print_console(f" Vérif ({len(valid_hotels)+1}/{TARGET_HOTELS_PER_CITY}) : {basic['hotel_name']}")
                    lat_d, lon_d, desc_d = deep_scrape_info(page_detail, basic['hotel_url'])
                    
                    l = basic['latitude'] if basic['latitude'] != 'N/A' else lat_d
                    o = basic['longitude'] if basic['longitude'] != 'N/A' else lon_d
                    
                    if l != 'N/A' and o != 'N/A' and desc_d != 'N/A':
                        basic['latitude'], basic['longitude'], basic['hotel_description'] = l, o, desc_d
                        valid_hotels.append(basic)
                    else:
                        print_console("  -> Incomplet, suivant...")
                    
                final_data.extend(valid_hotels)
            except Exception as e: print_console(f"Erreur ville: {e}")

        browser.close()

    if final_data:
        df = pd.DataFrame(final_data)
        for c in ['average_price', 'booking_score', 'latitude', 'longitude']:
            df[c] = pd.to_numeric(df[c].replace('N/A', np.nan), errors='coerce')
        
        df_f = pd.merge(df, df_villes[['id', 'latitude_city', 'longitude_city', 'avg_temp_c', 'median_pop']], left_on='city_id', right_on='id', how='left').drop(columns=['id'])
        df_f.reindex(columns=COLUMNS_ORDER).to_csv(OUTPUT_CSV_FILE, index=False, sep=';', encoding='utf-8', quoting=QUOTE_ALL)
        print_console(f"\nOK : {len(df_f)} hôtels sauvegardés.")

if __name__ == '__main__':
    run_scraper()