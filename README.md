# 🚦 Automated Annual Air Quality Monitoring for Bandung

## 📄 Overview

This project implements an end-to-end data engineering pipeline to process and monitor annual air quality metrics (PM2.5 & PM10) for Bandung using public data sources: BMKG, data.go.id, Nafas, and IQAir.

It supports environmental risk management by detecting abnormal pollution spikes and long-term trends automatically—empowering policymakers and communities to respond proactively.

The solution includes:

- Apache Airflow DAGs to orchestrate yearly workflows  
- Python scripts to extract, normalize, and stage raw data  
- Apache Spark batch jobs to compute yearly averages, maxima, and anomaly flags  
- Partitioned PostgreSQL warehouse for efficient querying  
- Interactive Streamlit dashboard for geographic trends and alerts  
- Email and Telegram notifications triggered by pollution thresholds

---

## 📁 Project Structure

```plaintext
bandung_airbatch/
├── dags/
│   ├── yearly_air_quality_pipeline.py          # Airflow DAG to schedule the annual pipeline
│   ├── scripts/
│   │   ├── extract_bmkg.py                     # Extract PM2.5/PM10 from BMKG API
│   │   ├── extract_datago.py                   # Download & parse from data.go.id
│   │   ├── extract_nafas.py                    # Extract data from Nafas PDF/Excel
│   │   ├── extract_iqair.py                    # Scrape AQI data from IQAir
│   │   └── load_to_staging.py                  # Load raw data into PostgreSQL staging table
│   └── sql/
│       ├── create_table_staging_raw_air_quality.sql
│       └── create_table_yearly_air_quality.sql
├── spark_jobs/
│   └── yearly_air_quality.py                   # Spark batch job for yearly aggregation
├── streamlit_app/
│   └── app.py                                  # Streamlit dashboard and alert logic
├── docker-compose.yml                          # Airflow, PostgreSQL, and Streamlit services
├── requirements.txt                            # Python dependencies
└── README.md                                   # Project documentation

🎯 Objectives

    Unify annual PM2.5 & PM10 data from BMKG, data.go.id, Nafas, and IQAir

    Compute year-over-year statistics: average, maximum, and outlier detection

    Flag abnormal pollution spikes when annual maxima exceed thresholds

    Provide interactive trend analysis and heatmaps via Streamlit dashboard

    Send automated alerts through email and Telegram

📚 Data Sources

    BMKG API: Daily JSON data for PM2.5 & PM10 (archived yearly)

 data.go.id:Annual CSV/JSON datasets

Nafas Indonesia: Yearly PDF/Excel sensor reports

IQAir Bandung: Scraped historical AQI and pollutant data

✨ Features

    🌐 Automated extraction from diverse formats: API, CSV, JSON, PDF, scraping

    🗄️ PostgreSQL staging for raw data

    ⚡ Apache Spark batch jobs for yearly aggregation

    📦 Partitioned PostgreSQL warehouse for fast queries

    🗺️ Streamlit dashboard with heatmaps, trend charts, and filters

    🔔 Email/Telegram alerts for pollution threshold breaches

    🔁 Airflow DAG for reproducible yearly runs

    🐳 Docker Compose to orchestrate services

🛠️ Tech Stack
Component	Tool
Orchestration	Apache Airflow
Extraction & ETL	Python (requests, pandas, tabula-py)
Batch Processing	Apache Spark
Staging & Warehouse	PostgreSQL
Visualization & Alerts	Streamlit, SMTP/Telegram Bot
Containerization	Docker & Docker Compose

+-----------------------------+
| Public Data Sources (Annual)|
| - BMKG API (JSON)           |
| - data.go.id (CSV/JSON)     |
| - Nafas (PDF/Excel)         |
| - IQAir Bandung (HTML/JSON) |
+-------------+---------------+
              |
              v
+-----------------------------+
| Airflow DAG Scheduler       |
| - Extract & Stage Raw Data  |
| - Spark Yearly Aggregation  |
| - Anomaly & Alert Logic     |
+-------------+---------------+
              |
              v
+-----------------------------+
| PostgreSQL Data Warehouse   |
| - warehouse.yearly_air_quality |
+-------------+---------------+
              |
              v
+-----------------------------+
| Streamlit Dashboard         |
| - Annual Trends & Heatmaps  |
| - Filters & Drill-down      |
| - Email/Telegram Alerts     |
+-----------------------------+

🚀 Getting Started

    Clone this repository

    Copy .env.example → .env and configure PostgreSQL and Telegram credentials

Run services with Docker Compose:
docker-compose up -d

Install Python dependencies inside Airflow container:
docker exec -it <airflow_container> pip install -r requirements.txt

Place DAG in dags/, extractor scripts in dags/scripts/, and Spark job in spark_jobs/

Access services:

Airflow UI > Localhost:
Streamlit UI > Localhost:
👤 Author

Project by Rafli Firmansyah — developed as part of an educational data engineering portfolio.
📝 License

This project is intended for educational and portfolio use only. Please review data provider usage policies before deploying publicly.
