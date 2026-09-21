# -*- coding: utf-8 -*-
"""
===============================================================================
PROJET KAYAK - BLOC 1 : PIPELINE D'INGENIERIE DE DONNEES & ETL CLOUD
SCRIPT : INGESTION CLOUD AWS S3 & POSTGRESQL (aws_ingestion.py)
===============================================================================
Architecture & Role :
  1. Data Lake (AWS S3) : Televersement du dataset brut (CSV) vers Amazon S3 via Boto3.
  2. Data Warehouse (PostgreSQL) : Ingestion relationnelle, creation du schema DDL
     et insertion atomique des donnees via psycopg2 / sqlalchemy.
  3. Verification & Integrite : Requetes SQL d'audit (comptage, metriques moyennes).
===============================================================================
"""

import os
import sys
import pandas as pd
import boto3
import psycopg2
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 1. Chargement securise des variables d'environnement depuis .env
load_dotenv()

# Configuration des fichiers et du stockage
INPUT_CSV_FILE = 'booking_hotels_v25_final.csv'
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'mlflow-artifacts-comcast-chris')
S3_FILE_KEY = os.getenv('S3_FILE_KEY', 'kayak/raw_data/booking_hotels_v25_final.csv')

# Configuration de la base de donnees PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
RDS_HOST = os.getenv('RDS_HOST')
RDS_PORT = int(os.getenv('RDS_PORT', 5432))
RDS_DBNAME = os.getenv('RDS_DBNAME', 'neondb')
RDS_USER = os.getenv('RDS_USER', 'neondb_owner')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_SSLMODE = os.getenv('RDS_SSLMODE', 'require')
RDS_TABLE_NAME = os.getenv('RDS_TABLE_NAME', 'kayak_hotels_data')


def upload_to_s3():
    """Televerse le dataset brut vers le Data Lake Amazon S3."""
    print("\n=======================================================")
    print("[ETAPE 1] TELEVERSEMENT VERS LE DATA LAKE (AWS S3)")
    print("=======================================================")

    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'eu-west-3')

    if not aws_access_key or not aws_secret_key:
        print("[ERREUR] Identifiants AWS manquants dans le fichier .env (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).")
        return False

    if not os.path.exists(INPUT_CSV_FILE):
        print(f"[ERREUR] Fichier source '{INPUT_CSV_FILE}' introuvable localement.")
        return False

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )

        file_size_kb = os.path.getsize(INPUT_CSV_FILE) / 1024
        print(f"[INFO] Preparation de l'envoi : '{INPUT_CSV_FILE}' ({file_size_kb:.1f} Ko)...")
        print(f"[INFO] Destination S3 : s3://{S3_BUCKET_NAME}/{S3_FILE_KEY}")

        s3_client.upload_file(INPUT_CSV_FILE, S3_BUCKET_NAME, S3_FILE_KEY)

        print(f"[SUCCESS S3] Donnees televersees avec succes sur Amazon S3 !")
        return True

    except Exception as e:
        print(f"[ERREUR S3] {e}")
        return False


def get_db_connection():
    """Etablit la connexion TCP/IP vers PostgreSQL."""
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL, connect_timeout=10)
    else:
        return psycopg2.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            database=RDS_DBNAME,
            user=RDS_USER,
            password=RDS_PASSWORD,
            sslmode=RDS_SSLMODE,
            connect_timeout=10
        )


def ingest_to_postgresql():
    """Cree la table relationnelle et insere les donnees dans PostgreSQL."""
    print("\n=======================================================")
    print("[ETAPE 2] INGESTION DANS LE DATA WAREHOUSE (POSTGRESQL)")
    print("=======================================================")

    if not os.path.exists(INPUT_CSV_FILE):
        print(f"[ERREUR] Fichier '{INPUT_CSV_FILE}' introuvable.")
        return False

    try:
        # 1. Lecture du DataFrame
        df = pd.read_csv(INPUT_CSV_FILE, sep=';', encoding='utf-8')
        print(f"[INFO] Donnees chargees : {len(df)} lignes et {len(df.columns)} colonnes.")

        # 2. Connexion a PostgreSQL
        print("[INFO] Connexion a la base de donnees PostgreSQL...")
        conn = get_db_connection()
        cur = conn.cursor()

        # 3. Creation du schema DDL (Idempotence avec DROP TABLE IF EXISTS)
        print(f"[INFO] Reinitialisation de la table '{RDS_TABLE_NAME}'...")
        cur.execute(f"DROP TABLE IF EXISTS {RDS_TABLE_NAME};")

        # Definition des types SQL adaptes
        ddl_query = f"""
        CREATE TABLE {RDS_TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            city_id VARCHAR(100),
            city VARCHAR(100),
            latitude_city NUMERIC(10, 6),
            longitude_city NUMERIC(10, 6),
            avg_temp_c NUMERIC(6, 2),
            median_pop NUMERIC(6, 4),
            hotel_name VARCHAR(255),
            hotel_description TEXT,
            booking_score NUMERIC(4, 2),
            average_price NUMERIC(10, 2),
            latitude NUMERIC(10, 6),
            longitude NUMERIC(10, 6)
        );
        """
        cur.execute(ddl_query)

        # 4. Insertion des donnees par lots (Batch Insertion securisee)
        print(f"[INFO] Insertion des {len(df)} enregistrements...")
        insert_query = f"""
        INSERT INTO {RDS_TABLE_NAME} (
            city_id, city, latitude_city, longitude_city, avg_temp_c,
            median_pop, hotel_name, hotel_description, booking_score,
            average_price, latitude, longitude
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        rows_to_insert = []
        for _, r in df.iterrows():
            def clean_val(v, is_num=False):
                if pd.isna(v) or v == 'N/A' or v == '':
                    return None
                if is_num:
                    try:
                        return float(str(v).replace(',', '.'))
                    except:
                        return None
                return str(v)

            row_tuple = (
                clean_val(r.get('city_id')),
                clean_val(r.get('city')),
                clean_val(r.get('latitude_city'), is_num=True),
                clean_val(r.get('longitude_city'), is_num=True),
                clean_val(r.get('avg_temp_c'), is_num=True),
                clean_val(r.get('median_pop'), is_num=True),
                clean_val(r.get('hotel_name')),
                clean_val(r.get('hotel_description')),
                clean_val(r.get('booking_score'), is_num=True),
                clean_val(r.get('average_price'), is_num=True),
                clean_val(r.get('latitude'), is_num=True),
                clean_val(r.get('longitude'), is_num=True)
            )
            rows_to_insert.append(row_tuple)

        cur.executemany(insert_query, rows_to_insert)
        conn.commit()

        # 5. Requetes d'audit et de verification
        print("\n--- AUDIT ET VERIFICATION POST-INGESTION ---")
        cur.execute(f"SELECT COUNT(*) FROM {RDS_TABLE_NAME};")
        total_rows = cur.fetchone()[0]
        print(f"[VERIF] Nombre total de lignes en base : {total_rows}")

        cur.execute(f"""
        SELECT 
            city, 
            COUNT(*) as nb_hotels, 
            ROUND(AVG(booking_score), 2) as note_moyenne, 
            ROUND(AVG(average_price), 2) as prix_moyen_eur,
            ROUND(AVG(avg_temp_c), 1) as temp_meteo_c
        FROM {RDS_TABLE_NAME}
        GROUP BY city
        ORDER BY temp_meteo_c DESC, note_moyenne DESC;
        """)

        stats = cur.fetchall()
        print("\n[SYNTHESE PAR VILLE] Top Destinations & Hotels :")
        print(f"{'Ville':<24} | {'Nb Hotels':<10} | {'Note Moy.':<10} | {'Prix Moy (EUR)':<14} | {'Meteo (C)':<10}")
        print("-" * 80)
        for s in stats:
            p_moy = f"{s[3]} EUR" if s[3] is not None else "N/A"
            print(f"{s[0]:<24} | {s[1]:<10} | {s[2]:<10} | {p_moy:<14} | {s[4]} C")

        cur.close()
        conn.close()
        print("\n[SUCCESS POSTGRESQL] Pipeline d'ingestion relationnelle termine avec succes !")
        return True

    except Exception as e:
        print(f"[ERREUR POSTGRESQL] {e}")
        return False


if __name__ == '__main__':
    print("=================================================================")
    print("EXECUTION DU PIPELINE D'INGESTION KAYAK (DATA LAKE + DATA WAREHOUSE)")
    print("=================================================================")

    # 1. Upload vers S3
    s3_ok = upload_to_s3()

    # 2. Ingestion vers PostgreSQL
    db_ok = ingest_to_postgresql()

    print("\n=======================================================")
    print(f"BILAN DU PIPELINE : S3 = {'SUCCES' if s3_ok else 'ECHEC'} | PostgreSQL = {'SUCCES' if db_ok else 'ECHEC'}")
    print("=======================================================")