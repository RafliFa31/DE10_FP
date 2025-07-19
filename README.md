##Automated Annual Air Quality Monitoring for Bandung
Overview

This project implements an end-to-end data engineering pipeline to process and monitor annual air quality metrics (PM2.5 & PM10) for Bandung using public sources (BMKG, data.go.id, Nafas, IQAir). It enables environmental risk management by automatically detecting abnormal pollution spikes and long-term trend shifts, empowering policymakers and communities to respond proactively.

The solution comprises ETL workflows orchestrated with Apache Airflow, Python scripts that extract and stage raw data in PostgreSQL, batch transformations with Apache Spark to calculate annual averages, maxima, and anomaly flags, storage of aggregated results in partitioned PostgreSQL tables, an interactive Streamlit dashboard for visualization, and proactive email/Telegram alerts whenever pollution thresholds are breached.

📁 Project Structure

bandung_airbatch/
├── dags/
│   ├── yearly_air_quality_pipeline.py        # Apache Airflow DAG for scheduling the annual pipeline
│   ├── scripts/
│   │   ├── extract_bmkg.py                   # Fetch yearly PM2.5/PM10 JSON from BMKG API
│   │   ├── extract_datago.py                 # Download & parse CSV/JSON from data.go.id
│   │   ├── extract_nafas.py                  # Extract tables from Nafas annual PDF/Excel
│   │   ├── extract_iqair.py                  # Scrape historical AQI & pollutant data from IQAir
│   │   └── load_to_staging.py                # Load raw JSON/CSV into `staging.raw_air_quality`
│   └── sql/
│       ├── create_table_staging_raw_air_quality.sql   # Schema for staging.raw_air_quality
│       └── create_table_yearly_air_quality.sql        # Schema for warehouse.yearly_air_quality
│
├── spark_jobs/
│   └── yearly_air_quality.py                # Spark batch job for annual aggregation (avg, max, outlier)
│
├── streamlit_app/
│   └── app.py                               # Streamlit dashboard & alert logic for annual metrics
│
├── docker-compose.yml                       # Defines Airflow, PostgreSQL, Streamlit services
├── requirements.txt                         # Python dependencies for extractors & Spark jobs
└── README.md                                # Project documentation & setup instructions

🎯 Objectives

- Unify annual PM2.5 & PM10 data from BMKG, data.go.id, Nafas, and IQAir  
- Compute year-over-year statistics: average, maximum, and outlier detection  
- Flag abnormal pollution spikes when annual maxima exceed thresholds  
- Provide interactive trend analysis and heatmaps via Streamlit dashboard  
- Send automated alerts through email and Telegram on threshold breaches  

📚 Data Source

- **BMKG API**: Archived daily PM2.5 & PM10 as JSON  
- **data.go.id**: Annual CSV/JSON downloads of public air-quality datasets  
- **Nafas Indonesia**: Yearly PDF/Excel reports from independent sensor network  
- **IQAir Bandung**: Scraped historical AQI, PM2.5 & PM10 data  

✨ Features

- 🌐 Automated extraction from APIs, CSV/JSON, PDF/Excel, and web scraping  
- 🗄️ PostgreSQL staging for raw JSON/CSV data  
- ⚡ Apache Spark batch jobs to aggregate annual metrics  
- 📦 Partitioned PostgreSQL warehouse for efficient year-based queries  
- 🗺️ Streamlit dashboard with interactive charts, heatmaps, and filters  
- 🔔 Proactive email & Telegram alerts when pollution thresholds are exceeded  
- 🔁 Apache Airflow DAG for scheduled, reproducible annual runs  
- 🐳 Docker Compose to orchestrate Airflow, Postgres, and Streamlit  

🛠️ Tech Stack

| Component            | Tool                                  |
|----------------------|---------------------------------------|
| Orchestration        | Apache Airflow                        |
| Extraction & ETL     | Python (requests, pandas, tabula-py)  |
| Batch Processing     | Apache Spark                          |
| Staging & Warehouse  | PostgreSQL                            |
| Visualization & Alerts | Streamlit, SMTP/Telegram Bot       |
| Containerization     | Docker & Docker Compose               |

Architecture
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
| - Spark Annual Aggregation  |
| - Anomaly & Alert Generation|
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
| - Annual Trend Analysis     |
| - Kecamatan Heatmaps        |
| - Filters & Drill-down      |
| - Email & Telegram Alerts   |
+-----------------------------+

Getting Started
- Clone this repository
- Copy .env.example to .env, fill in PostgreSQL and Telegram credentials
- Run docker-compose up -d to launch Airflow, PostgreSQL, and Streamlit
- Install Python dependencies in the Airflow container:
docker exec -it <airflow_container> pip install -r requirements.txt
- Place your DAG in dags/, extractor scripts in dags/scripts/, and Spark job in spark_jobs/
- Access services:
Airflow: http://localhost:8080
Streamlit: http://localhost:8501


##Author

Project by Rafli Firmansyah — developed as an educational portfolio project in data engineering.
License

This project is for educational and portfolio purposes only. Please review data provider usage policies before any public deployment.
