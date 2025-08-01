# 🚦 Automated Annual Air Quality Monitoring for Bandung

## 📄 Overview

Proyek ini mengimplementasikan sebuah pipeline data end-to-end untuk memonitor kualitas udara tahunan (PM2.5) di Bandung. Dimulai dengan data historis dari laporan publik sebagai fondasi, arsitektur ini dirancang untuk dapat diperluas dengan sumber data dinamis seperti API di masa depan. Tujuan utamanya adalah mengotomatiskan analisis tren jangka panjang untuk mendukung kebijakan lingkungan dan memberdayakan masyarakat dengan data yang mudah diakses.

Pipeline ini diorkestrasi oleh Apache Airflow, menggunakan Python untuk ekstraksi data ke Neon DB (PostgreSQL) yang berfungsi sebagai staging area dan data warehouse. Transformasi dan agregasi data dijalankan oleh Apache Spark, dengan hasil akhir yang divisualisasikan pada dashboard Streamlit interaktif. Platform ini juga dirancang untuk dapat mengirimkan notifikasi otomatis melalui Email atau Telegram jika terdeteksi tingkat polusi yang melebihi ambang batas.
* kak boleh gak ya dilulusin dulu, masihh ingin dikembangin dan benerin karena ini kurang banget, nanti pas dikoreksi masih kurang , aku bakal langsung benerin, tapi benerann kak izin banget buat dilulusin :(
---

## 📁 Project Structure

```plaintext
:\Users\NoXox\Documents\bandung_airbatch/
├── data/
│   ├── Kesehatan_Udara_Bandung_2022.xlsx  # Perhatikan: ini adalah file .xlsx, bukan .csv
│   ├── Kesehatan_Udara_Bandung_2023.xlsx
│   ├── Kesehatan_Udara_Bandung_2024.xlsx
│   └── Kesehatan_Udara_Bandung_2025.xlsx
├── dags/
│   ├── Dag_Bandung_yearly_air_quality_pipeline.py # Nama file DAG berbeda
│   ├── Python Script_extract_local_csv.py         # Nama file script Python berbeda
│   └── create_table_staging_raw_air_quality.sql   # SQL file ini langsung di dags/, bukan di dags/sql/
├── spark_jobs/
├── streamlit_app/
│   ├── Streamlit requirements.txt                 # Nama file requirements Streamlit berbeda
│   └── Streamlit.py                               # Nama file aplikasi Streamlit berbeda
├── docker-compose.yml
├── PySpark Job_Bandung_yearly_air_quality.py      # File PySpark ini ada di root, bukan di spark_jobs/
└── requirements.txt



##Objectives

- Mengkonsolidasikan data kualitas udara tahunan (PM2.5) dari file CSV yang disediakan.
- Menghitung rata-rata tahunan, nilai maksimum, dan mendeteksi outlier untuk metrik polusi.
- Menandai tahun-tahun dengan lonjakan polusi yang tidak biasa berdasarkan logika ambang batas.
- Memvisualisasikan tren jangka panjang via dashboard.
- Memberi tahu pemangku kepentingan secara otomatis melalui email atau Telegram.

📚 Data Sources

-website databooks (https://databoks.katadata.co.id/layanan-konsumen-kesehatan/statistik/3b72788adeb2920/kualitas-udara-di-kota-besar-indonesia-buruk-jauh-dari-standar-who)
-BMKG API – archived daily JSON data
-data/go.id – downloadable CSV/JSON datasets
-Nafas Indonesia – sensor reports in PDF/Excel format
-IQAir Bandung – scraped AQI and pollutant archive
*untuk sekarang dataset yang saya gunakan dari nafas indonesia

Features
- 🌐 Ekstraksi data otomatis dari file CSV yang disediakan (dengan potensi ekspansi ke API dan web scraping di masa depan).
-🗄️ Staging PostgreSQL dan warehouse terpartisi untuk kueri cepat.
-⚡ Spark batch jobs untuk menghitung statistik tahunan.
-📊 Dashboard Streamlit interaktif dengan filter dan bagan.
-🔔 Peringatan via Telegram/email ketika polusi melebihi ambang batas.
-🔁 Penjadwalan yang dapat direproduksi dengan Apache Airflow.
-🐳 Penyiapan Docker Compose untuk deployment.

🛠️ Tech Stack
Component            Tool
-------------------- --------------------------------------
Orchestration        Apache Airflow
Extraction & ETL     Python (requests, pandas, tabula-py)
Batch Processing     Apache Spark
Data Storage         PostgreSQL
Visualization        Streamlit
Alerting             SMTP, Telegram Bot
Containerization     Docker, Docker Compose

[1. Sumber Data Awal]
    (untuk awal sekarang file excel dulu, kedepannya ditingkatin berbagai sumber kak, masih bingung :()
        |
        v
[2. Ekstraksi Data] ——— (Diorkestrasi oleh 💨 Airflow)
    (Python Script)
        |
        v
[3. Staging Area]
    (Neon DB (PostgreSQL) 🐘)
        |
        v
[4. Transformasi Data] ——— (Diorkestrasi oleh 💨 Airflow)
    (Apache Spark ✨)
        |
        v
[5. Data Warehouse]
    (Neon DB (PostgreSQL) 🐘)
        |
        v
[6. Visualisasi & Aksi]
    (Streamlit Dashboard 📊)


⚙️⚙️ Pipeline Overview
1. ETL (Airflow DAG yearly_air_quality_pipeline)
Extract: Membaca data dari file CSV tahunan yang disediakan 
Load (Staging): Menyimpan data mentah ke tabel staging.raw_air_quality di PostgreSQL. Analytics Generation (Spark Job)
Transform: Membaca data dari staging, memvalidasi skema, dan melakukan transformasi dasar (misal: mengganti nama kolom).
Load (Warehouse): Menyimpan data matang yang sudah diolah ke tabel warehouse.fact_yearly_air_quality.

Visualization (Streamlit)
Query: Aplikasi Streamlit melakukan kueri langsung ke tabel warehouse di PostgreSQL.
Display: Menampilkan tren kualitas udara tahunan dalam bentuk grafik batang dan tabel interaktif. Koneksi Database (PostgreSQL)

psql 'postgresql://neondb_owner:npg_odbj5JHY0pwO@ep-cold-grass-a18xlnz0-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

Keterbatasan & Rencana Pengembangan
Untuk pengembangan di masa depan, terdapat beberapa keterbatasan pada platform saat ini yang bisa menjadi peluang untuk perbaikan:

Keterbatasan Saat Ini (Limitations)
- Dataset statis, belum mendukung incremental load atau streaming.
- Tidak semua field (seperti tanggal transaksi) diproses secara time-series (fokus saat ini pada agregasi tahunan).
- Belum terhubung ke BI tools lain seperti Looker/Power BI.
- Proses ekstraksi data masih bergantung pada file CSV yang disiapkan secara semi-manual.
- Platform hanya berjalan dalam mode batch (tahunan), sehingga cocok untuk analisis historis tetapi tidak untuk pemantauan real-time.
- Dashboard Streamlit menyajikan visualisasi data dasar yang informatif.

Rencana Pengembangan (Recommendations)
- Tambah time dimension untuk analitik per bulan atau per hari, memungkinkan analisis tren yang lebih granular.
- Tambah scheduler untuk export PNG otomatis dari Metabase (atau alat visualisasi lain yang terhubung).
- Sinkronisasi data dari API eksternal (misal BMKG, OpenAQ) untuk mencapai otomatisasi penuh dan memperkaya data.
- Jika kebutuhan bisnis berkembang, platform dapat diperluas dengan menambahkan alur streaming menggunakan teknologi seperti Apache Kafka dan Spark Streaming untuk notifikasi yang lebih cepat.
- Menambahkan fitur analitik yang lebih canggih di masa depan, seperti analisis prediktif (forecasting) untuk memperkirakan kualitas udara atau analisis korelasi dengan data lain (misalnya, data cuaca atau lalu lintas).

👤 Author
Project by Rafli Firmansyah — dibangun untuk tujuan edukasi dan pengembangan portofolio di bidang data engineering.
📝 License
Proyek ini ditujukan untuk penggunaan edukasi dan portofolio.
