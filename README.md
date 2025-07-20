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
+-------------------------------------+
| 1. Public Data Sources              |
|    (API, CSV, PDF, Web)             |
+------------------+------------------+
                   |
                   v (Diperintah oleh Airflow)
+-------------------------------------+
| 2. Python Extraction Scripts        |
|    (Mengambil & menyimpan data mentah)|
+------------------+------------------+
                   |
                   v
+-------------------------------------+
| 3. Staging Area (PostgreSQL)        |
|    (Tempat data mentah dikumpulkan) |
+------------------+------------------+
                   |
                   v (Diperintah oleh Airflow)
+-------------------------------------+
| 4. Apache Spark Batch Job           |
|    - Membersihkan data mentah       |
|    - Menghitung agregat (avg, max)  |
|    - Menyimpan data matang          |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
| 5. Data Warehouse (PostgreSQL)      |
|    (Data bersih & siap dianalisis)  |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
| 6. Streamlit Dashboard              |
|    (Membaca & memvisualisasikan data)|
+-------------------------------------+

🚀 Getting Started

Clone this repository
Copy .env.example → .env and provide PostgreSQL and Telegram credentials

Start services:
docker-compose up -d

Install Python dependencies:
docker exec -it <airflow_container> pip install -r requirements.txt

Place your DAG in dags/, scripts in dags/scripts/, and Spark job in spark_jobs/

Access services:

    Airflow: http://localhost:8080

    Streamlit: http://localhost:8501


👤 Author

Project by Rafli Firmansyah — built for educational and portfolio development in data engineering.
📝 License

This project is intended for educational and portfolio use only. Please consult the terms of use for BMKG, data.go.id, Nafas, and IQAir before public deployment.
