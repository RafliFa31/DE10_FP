import pandas as pd
import psycopg2
import os
import sys
from urllib.parse import urlparse

def extract_and_load_to_staging(neon_db_conn_string):
    """
    Mengekstrak data dari file CSV lokal dan memuatnya ke tabel staging di Neon DB.
    """
    print("Starting data extraction from local CSVs...")

    # Daftar file CSV yang akan dibaca
    csv_files = [
        '/opt/airflow/data/Kesehatan_Udara_Bandung_2022.xlsx - Sheet1.csv',
        '/opt/airflow/data/Kesehatan_Udara_Bandung_2023.xlsx - Sheet1.csv',
        '/opt/airflow/data/Kesehatan_Udara_Bandung_2024.xlsx - Sheet1.csv',
        '/opt/airflow/data/Kesehatan_Udara_Bandung_2025.xlsx - Sheet1.csv'
    ]

    all_data = []
    for file_path in csv_files:
        if os.path.exists(file_path):
            print(f"Reading file: {file_path}")
            # Baca CSV, pastikan header sesuai
            df = pd.read_csv(file_path)
            all_data.append(df)
        else:
            print(f"Warning: File not found at {file_path}. Skipping.")

    if not all_data:
        print("No CSV files found or processed. Exiting.")
        return

    # Gabungkan semua data menjadi satu DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"Combined data shape: {combined_df.shape}")
    print("Combined data head:")
    print(combined_df.head())

    # Bersihkan nama kolom (opsional, jika ada spasi atau karakter khusus)
    combined_df.columns = combined_df.columns.str.strip().str.lower().str.replace('.', '', regex=False).str.replace(' ', '_', regex=False)

    # Pastikan kolom yang dibutuhkan ada
    required_columns = ['tahun', 'kota', 'parameter', 'nilai', 'satuan']
    if not all(col in combined_df.columns for col in required_columns):
        print(f"Error: Missing one or more required columns. Found: {combined_df.columns.tolist()}, Required: {required_columns}")
        return

    # Konversi tipe data jika diperlukan
    combined_df['tahun'] = pd.to_numeric(combined_df['tahun'], errors='coerce').astype('Int64')
    combined_df['nilai'] = pd.to_numeric(combined_df['nilai'], errors='coerce')

    # Hapus baris dengan nilai NaN di kolom penting
    combined_df.dropna(subset=['tahun', 'nilai'], inplace=True)

    # Parse connection string untuk psycopg2
    result = urlparse(neon_db_conn_string)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port if result.port else 5432
    sslmode = "require" if "sslmode=require" in neon_db_conn_string else "prefer" # Extract sslmode

    try:
        conn = psycopg2.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port,
            sslmode=sslmode
        )
        cur = conn.cursor()

        # Hapus data lama di tabel staging sebelum memasukkan yang baru
        cur.execute("TRUNCATE TABLE staging.raw_air_quality;")
        print("Truncated staging.raw_air_quality table.")

        # Masukkan data ke tabel staging
        for index, row in combined_df.iterrows():
            insert_query = """
            INSERT INTO staging.raw_air_quality (tahun, kota, parameter, nilai, satuan)
            VALUES (%s, %s, %s, %s, %s);
            """
            cur.execute(insert_query, (
                row['tahun'],
                row['kota'],
                row['parameter'],
                row['nilai'],
                row['satuan']
            ))
        conn.commit()
        print(f"Successfully loaded {len(combined_df)} rows to staging.raw_air_quality.")

    except Exception as e:
        print(f"Error connecting to or loading data to Neon DB: {e}")
        conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_local_csv.py <NEON_DB_CONN_STRING>")
        sys.exit(1)
    neon_db_conn_string = sys.argv[1]
    extract_and_load_to_staging(neon_db_conn_string)