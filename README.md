# 🚦 Automated Annual Air Quality Monitoring for Bandung

## 📄 Overview

This project implements an end-to-end data engineering pipeline to process and monitor annual air quality metrics (PM2.5 & PM10) for Bandung using public sources (BMKG, data.go.id, Nafas, IQAir). It supports environmental risk management by detecting abnormal pollution spikes and long-term trend shifts automatically, enabling timely response by policymakers and communities.

The solution includes:

- ETL workflows orchestrated with Apache Airflow  
- Python scripts to extract and stage raw data in PostgreSQL  
- Batch transformations using Apache Spark to compute yearly statistics and anomaly flags  
- Partitioned PostgreSQL warehouse  
- Interactive Streamlit dashboard for data visualization  
- Proactive alerts via email and Telegram when pollution thresholds are breached  

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

    Unify PM2.5 & PM10 data from BMKG, data.go.id, Nafas, and IQAir

    Compute annual statistics: average, maximum, and anomaly detection

    Flag abnormal pollution spikes when maxima exceed thresholds

    Visualize yearly trends and geographic patterns via Streamlit

    Send automatic alerts through email and Telegram

📚 Data Sources

    BMKG API: Daily JSON data for PM2.5/PM10 (archived yearly)

