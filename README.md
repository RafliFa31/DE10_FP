# 🚦 Automated Annual Air Quality Monitoring for Bandung

## 📄 Overview

This project implements an end-to-end data engineering pipeline to process and monitor annual air quality metrics (PM2.5 & PM10) for Bandung using public sources (BMKG, data.go.id, Nafas, IQAir). It supports environmental risk management by automatically detecting abnormal pollution spikes and long-term trends, empowering policymakers and communities to respond proactively.

The pipeline uses Apache Airflow to orchestrate yearly ETL workflows, Python scripts to extract and stage data in PostgreSQL, Apache Spark to compute aggregated annual statistics, and a Streamlit dashboard for interactive visualization and alerting. Threshold breaches automatically trigger notifications via email or Telegram.

---

## 📁 Project Structure

```plaintext
bandung_airbatch/
├── dags/
│   ├── yearly_air_quality_pipeline.py           # Airflow DAG for annual workflow
│   ├── scripts/
│   │   ├── extract_bmkg.py                      # Fetch JSON from BMKG
│   │   ├── extract_datago.py                    # Download & parse CSV/JSON from data.go.id
│   │   ├── extract_nafas.py                     # Parse air-quality tables from PDF/Excel
│   │   ├── extract_iqair.py                     # Scrape historical AQI & pollutant data
│   │   └── load_to_staging.py                   # Load raw data into PostgreSQL staging
│   └── sql/
│       ├── create_table_staging_raw_air_quality.sql
│       └── create_table_yearly_air_quality.sql
├── spark_jobs/
│   └── yearly_air_quality.py                    # Spark job for annual aggregation
├── streamlit_app/
│   └── app.py                                   # Streamlit dashboard & alert logic
├── docker-compose.yml                           # Multi-container orchestration
├── requirements.txt                             # Python dependencies
└── README.md                                     # Project documentation



##Objectives

    Consolidate annual air-quality data (PM2.5 & PM10) from multiple public sources

    Calculate yearly average, maximum, and detect outliers for pollution metrics

    Flag years with unusual pollution spikes based on threshold logic

    Visualize long-term trends and geographic patterns via dashboard

    Notify stakeholders automatically via email or Telegram

📚 Data Sources

    BMKG API – archived daily JSON data
    data/go.id – downloadable CSV/JSON datasets
    Nafas Indonesia – sensor reports in PDF/Excel format
    IQAir Bandung – scraped AQI and pollutant archive

    ✨ Features

    🌐 Automated data extraction from API, CSV, JSON, PDF, and web scraping

    🗄️ PostgreSQL staging and partitioned warehouse for fast queries

    ⚡ Spark batch jobs to compute yearly stats

    📊 Interactive Streamlit dashboard with filters, charts, and heatmaps

    🔔 Alerts via Telegram/email when pollution exceeds thresholds

    🔁 Reproducible scheduling with Apache Airflow

    🐳 Docker Compose setup for deployment

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

📐 Architecture
1. Sumber Data Awal]
     (File CSV)
          |
          v
[2. Ekstraksi Data] ——— (Diperintah oleh 💨 Airflow)
    (Python Script)
          |
          v
[3. Staging Area]
   (PostgreSQL 🐘)
          |
          v
[4. Transformasi Data] — (Diperintah oleh 💨 Airflow)
  (Apache Spark ✨)
          |
          v
[5. Data Warehouse]
   (PostgreSQL 🐘)
          |
          v
[6. Visualisasi & Aksi]
 (Streamlit Dashboard 📊)

Pipeline Overview

    ETL (Airflow DAG air_quality_etl_pipeline)

        Extract: Membaca data dari file bandung_air_quality.csv.

        Load (Staging): Menyimpan data mentah ke tabel staging.raw_air_quality di PostgreSQL.

    Analytics Generation (Spark Job)

        Transform: Membaca data dari staging, memvalidasi skema, dan melakukan transformasi dasar (misal: mengganti nama kolom).

        Load (Warehouse): Menyimpan data matang yang sudah diolah ke tabel warehouse.fact_yearly_air_quality.

    Visualization (Streamlit)

        Query: Aplikasi Streamlit melakukan kueri langsung ke tabel warehouse di PostgreSQL.

        Display: Menampilkan tren kualitas udara tahunan dalam bentuk grafik batang dan tabel interaktif.1

Keterbatasan & Rekomendasi (Limitations & Recommendations)
Untuk pengembangan di masa depan, terdapat beberapa keterbatasan pada platform saat ini yang bisa menjadi peluang untuk perbaikan:
Keterbatasan Sumber Data: 
Kondisi Saat Ini: Proses ekstraksi data masih bergantung pada file CSV yang disiapkan secara semi-manual.
Rekomendasi: Mengintegrasikan pipeline secara langsung dengan API publik (BMKG) dan teknik web scraping untuk mencapai otomatisasi penuh dan memperkaya data.

Keterbatasan Model Pemrosesan:
Kondisi Saat Ini: Platform hanya berjalan dalam mode batch (tahunan), sehingga cocok untuk analisis historis tetapi tidak untuk pemantauan real-time.
Rekomendasi: Jika kebutuhan bisnis berkembang, platform dapat diperluas dengan menambahkan alur streaming menggunakan teknologi seperti Apache Kafka dan Spark Streaming untuk notifikasi yang lebih cepat.
Keterbatasan Fitur Dashboard:
Kondisi Saat Ini: Dashboard Streamlit menyajikan visualisasi data dasar yang informatif.
Rekomendasi: Menambahkan fitur analitik yang lebih canggih di masa depan, seperti analisis prediktif (forecasting) untuk memperkirakan kualitas udara atau analisis korelasi dengan data lain (misalnya, data cuaca atau lalu lintas).



👤 Author

Project by Rafli Firmansyah — built for educational and portfolio development in data engineering.
📝 License

This project is intended for educational and portfolio use only. Please consult the terms of use for BMKG, data.go.id, Nafas, and IQAir before public deployment.
