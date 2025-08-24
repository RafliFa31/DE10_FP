# 🚦 Automated Annual Air Quality Monitoring for Bandung

## 📄 Overview

Proyek ini mengimplementasikan sebuah pipeline data end-to-end untuk memonitor kualitas udara tahunan (PM2.5) di Bandung. Dimulai dengan data historis dari laporan publik sebagai fondasi, arsitektur ini dirancang untuk dapat diperluas dengan sumber data dinamis seperti API di masa depan. Tujuan utamanya adalah mengotomatisasi analisis tren jangka panjang untuk mendukung kebijakan lingkungan dan memberdayakan masyarakat dengan data yang mudah diakses.

Pipeline ini diorkestrasi oleh Apache Airflow, menggunakan Python untuk ekstraksi data ke Neon DB (PostgreSQL) yang berfungsi sebagai staging area dan data warehouse. Transformasi dan agregasi data dijalankan oleh Apache Spark, dengan hasil akhir yang divisualisasikan pada dashboard Streamlit interaktif. Platform ini juga dirancang untuk dapat mengirimkan notifikasi otomatis melalui Email atau Telegram jika terdeteksi tingkat polusi yang melebihi ambang batas.

---

## 🎯 Objectives

- Mengkonsolidasikan data kualitas udara tahunan (PM2.5) dari file Excel yang disediakan
- Menghitung rata-rata tahunan, nilai maksimum, dan mendeteksi outlier untuk metrik polusi
- Menandai tahun-tahun dengan lonjakan polusi yang tidak biasa berdasarkan logika ambang batas
- Memvisualisasikan tren jangka panjang via dashboard interaktif
- Memberi tahu pemangku kepentingan secara otomatis melalui email atau Telegram

---

## 📁 Project Structure

```
bandung_airbatch/
├── data/
│   ├── Kesehatan_Udara_Bandung_2022.xlsx
│   ├── Kesehatan_Udara_Bandung_2023.xlsx
│   ├── Kesehatan_Udara_Bandung_2024.xlsx
│   └── Kesehatan_Udara_Bandung_2025.xlsx
├── dags/
│   ├── Dag_Bandung_yearly_air_quality_pipeline.py
│   ├── Python Script_extract_local_csv.py
│   └── create_table_staging_raw_air_quality.sql
├── spark_jobs/
├── streamlit_app/
│   ├── Streamlit requirements.txt
│   └── Streamlit.py
├── docker-compose.yml
├── PySpark Job_Bandung_yearly_air_quality.py
└── requirements.txt
```

---

## 📚 Data Sources

Saat ini menggunakan dataset dari **Nafas Indonesia** dalam format Excel. Untuk pengembangan masa depan, akan diintegrasikan dengan:

- [Databoks](https://databoks.katadata.co.id/layanan-konsumen-kesehatan/statistik/3b72788adeb2920/kualitas-udara-di-kota-besar-indonesia-buruk-jauh-dari-standar-who)
- BMKG API – archived daily JSON data
- data.go.id – downloadable CSV/JSON datasets
- Nafas Indonesia – sensor reports in PDF/Excel format
- IQAir Bandung – scraped AQI and pollutant archive

---

## ✨ Features

- 🌐 **Ekstraksi data otomatis** dari file Excel yang disediakan (dengan potensi ekspansi ke API dan web scraping di masa depan)
- 🗄️ **Staging PostgreSQL** dan warehouse terpartisi untuk kueri cepat
- ⚡ **Spark batch jobs** untuk menghitung statistik tahunan
- 📊 **Dashboard Streamlit interaktif** dengan filter dan bagan
- 🔔 **Peringatan otomatis** via Telegram/email ketika polusi melebihi ambang batas
- 🔁 **Penjadwalan otomatis** dengan Apache Airflow
- 🐳 **Docker Compose** untuk deployment yang mudah

---

## 🛠️ Tech Stack

| Component | Tool |
|-----------|------|
| **Orchestration** | Apache Airflow |
| **Extraction & ETL** | Python (requests, pandas, tabula-py) |
| **Batch Processing** | Apache Spark |
| **Data Storage** | PostgreSQL (Neon DB) |
| **Visualization** | Streamlit |
| **Alerting** | SMTP, Telegram Bot |
| **Containerization** | Docker, Docker Compose |

---

## 🔄 Pipeline Overview

```
[1. Sumber Data Awal]
    (File Excel)
        ↓
[2. Ekstraksi Data] ——— (Diorkestrasi oleh 💨 Airflow)
    (Python Script)
        ↓
[3. Staging Area]
    (Neon DB PostgreSQL 🐘)
        ↓
[4. Transformasi Data] ——— (Diorkestrasi oleh 💨 Airflow)
    (Apache Spark ✨)
        ↓
[5. Data Warehouse]
    (Neon DB PostgreSQL 🐘)
        ↓
[6. Visualisasi & Aksi]
    (Streamlit Dashboard 📊)
```

### Workflow Detail

1. **ETL (Airflow DAG yearly_air_quality_pipeline)**
   - **Extract**: Membaca data dari file Excel tahunan yang disediakan
   - **Load (Staging)**: Menyimpan data mentah ke tabel `staging.raw_air_quality` di PostgreSQL

2. **Analytics Generation (Spark Job)**
   - **Transform**: Membaca data dari staging, memvalidasi skema, dan melakukan transformasi dasar
   - **Load (Warehouse)**: Menyimpan data matang yang sudah diolah ke tabel `warehouse.fact_yearly_air_quality`

3. **Visualization (Streamlit)**
   - **Query**: Aplikasi Streamlit melakukan kueri langsung ke tabel warehouse di PostgreSQL
   - **Display**: Menampilkan tren kualitas udara tahunan dalam bentuk grafik batang dan tabel interaktif

---

## 🗄️ Database Connection

```bash
psql 'postgresql://neondb_owner:npg_odbj5JHY0pwO@ep-cold-grass-a18xlnz0-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
```

---

## ⚠️ Keterbatasan & Rencana Pengembangan

### Keterbatasan Saat Ini

- Dataset statis, belum mendukung incremental load atau streaming
- Tidak semua field (seperti tanggal transaksi) diproses secara time-series (fokus saat ini pada agregasi tahunan)
- Belum terhubung ke BI tools lain seperti Looker/Power BI
- Proses ekstraksi data masih bergantung pada file Excel yang disiapkan secara semi-manual
- Platform hanya berjalan dalam mode batch (tahunan), sehingga cocok untuk analisis historis tetapi tidak untuk pemantauan real-time

### Rencana Pengembangan

- **Time Dimension Enhancement**: Menambah analitik per bulan atau per hari untuk analisis tren yang lebih granular
- **Automated Reporting**: Scheduler untuk export PNG otomatis dari dashboard
- **API Integration**: Sinkronisasi data dari API eksternal (BMKG, OpenAQ) untuk otomatisasi penuh
- **Real-time Processing**: Implementasi streaming menggunakan Apache Kafka dan Spark Streaming
- **Advanced Analytics**: Analisis prediktif (forecasting) dan korelasi dengan data cuaca atau lalu lintas
- **BI Tools Integration**: Koneksi ke Looker, Power BI, atau tools visualisasi enterprise lainnya

---

## 🚀 Quick Start

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd bandung_airbatch
   ```

2. **Setup environment**
   ```bash
   docker-compose up -d
   ```

3. **Access services**
   - Airflow: `http://localhost:8080`
   - Streamlit: `http://localhost:8501`

---

## 👤 Author

**Rafli Firmansyah**  
Project ini dibangun untuk tujuan edukasi dan pengembangan portofolio di bidang data engineering.

---

## 📝 License

Proyek ini ditujukan untuk penggunaan edukasi dan portofolio.

---

## 📞 Support

Jika ada pertanyaan atau saran pengembangan, silakan buat issue atau hubungi penulis.
