import streamlit as st
import pandas as pd
import psycopg2
import os
import plotly.express as px
from urllib.parse import urlparse

st.set_page_config(layout="wide", page_title="Bandung Air Quality Dashboard")

# Mengambil connection string Neon DB dari environment variable
NEON_DB_CONN_STRING = os.getenv('NEON_DB_CONN_STRING')

if not NEON_DB_CONN_STRING:
    st.error("NEON_DB_CONN_STRING environment variable not set. Please configure it in docker-compose.yml.")
    st.stop()

def get_db_details_from_conn_string(conn_string):
    """
    Mengekstrak detail database dari connection string.
    """
    result = urlparse(conn_string)
    return {
        "user": result.username,
        "password": result.password,
        "database": result.path[1:],
        "host": result.hostname,
        "port": result.port if result.port else 5432,
        "sslmode": "require" if "sslmode=require" in conn_string else "prefer"
    }

@st.cache_data(ttl=600) # Cache data selama 10 menit
def load_data_from_warehouse():
    """
    Memuat data kualitas udara dari tabel warehouse di Neon DB.
    """
    db_details = get_db_details_from_conn_string(NEON_DB_CONN_STRING)
    conn = None
    try:
        conn = psycopg2.connect(
            host=db_details['host'],
            database=db_details['database'],
            user=db_details['user'],
            password=db_details['password'],
            port=db_details['port'],
            sslmode=db_details['sslmode']
        )
        query = "SELECT tahun, kota, parameter, avg_nilai, max_nilai, min_nilai, satuan FROM warehouse.fact_yearly_air_quality ORDER BY tahun ASC;"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error loading data from database: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

st.title("📊 Monitoring Kualitas Udara Tahunan Bandung (PM2.5)")
st.markdown("Dashboard ini menyajikan tren kualitas udara PM2.5 tahunan di Kota Bandung.")

df_air_quality = load_data_from_warehouse()

if not df_air_quality.empty:
    st.subheader("Data Kualitas Udara Tahunan (PM2.5)")
    st.dataframe(df_air_quality)

    # Visualisasi Tren PM2.5 Tahunan
    st.subheader("Tren Rata-rata PM2.5 Tahunan")
    fig = px.bar(df_air_quality, x='tahun', y='avg_nilai',
                 title='Rata-rata Konsentrasi PM2.5 Tahunan di Bandung',
                 labels={'tahun': 'Tahun', 'avg_nilai': 'Rata-rata PM2.5 (ug/m3)'},
                 hover_data=['max_nilai', 'min_nilai', 'satuan'])
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Deteksi Outlier Sederhana (Contoh)
    st.subheader("Deteksi Potensi Lonjakan Polusi")
    threshold_pm25 = 40 # Contoh ambang batas untuk PM2.5 (bisa disesuaikan)
    outliers = df_air_quality[df_air_quality['avg_nilai'] > threshold_pm25]

    if not outliers.empty:
        st.warning(f"⚠️ Peringatan: Rata-rata PM2.5 melebihi ambang batas {threshold_pm25} ug/m3 pada tahun-tahun berikut:")
        st.dataframe(outliers)
        # Di sini kamu bisa menambahkan logika untuk mengirim notifikasi Email/Telegram
        # Contoh:
        # if st.button("Kirim Notifikasi"):
        #     send_alert_telegram(outliers)
        #     send_alert_email(outliers)
        #     st.success("Notifikasi terkirim!")
    else:
        st.info(f"✅ Kualitas udara rata-rata tahunan di bawah ambang batas {threshold_pm25} ug/m3.")

else:
    st.info("Data kualitas udara belum tersedia atau gagal dimuat. Pastikan pipeline Airflow sudah berjalan.")

