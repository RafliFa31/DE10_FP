from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import os
import logging

# Konfigurasi logging
log = logging.getLogger(__name__)

# Mengambil connection string Neon DB dari environment variable
# Pastikan NEON_DB_CONN_STRING diatur di docker-compose.yml
NEON_DB_CONN_STRING = os.getenv('NEON_DB_CONN_STRING')
if not NEON_DB_CONN_STRING:
    raise ValueError("NEON_DB_CONN_STRING environment variable not set.")

def _execute_sql_file(sql_file_path, conn_id='postgres_default'):
    """
    Fungsi helper untuk mengeksekusi file SQL menggunakan PostgresHook.
    """
    log.info(f"Executing SQL file: {sql_file_path}")
    pg_hook = PostgresHook(postgres_conn_id=conn_id)
    with open(sql_file_path, 'r') as f:
        sql_commands = f.read()
    pg_hook.run(sql_commands)
    log.info(f"Successfully executed {sql_file_path}")

with DAG(
    dag_id='yearly_air_quality_pipeline',
    start_date=days_ago(1),
    schedule_interval=None, # Jalankan secara manual atau dengan trigger
    catchup=False,
    tags=['air_quality', 'bandung', 'etl'],
    doc_md="""
    ### Pipeline Kualitas Udara Tahunan Bandung
    DAG ini mengorkestrasi proses ETL untuk data kualitas udara tahunan PM2.5 di Bandung.
    Meliputi:
    1. Inisialisasi tabel di Neon DB (staging dan warehouse).
    2. Ekstraksi data dari file CSV lokal ke tabel staging.
    3. Transformasi dan agregasi data menggunakan Apache Spark, lalu memuat ke tabel warehouse.
    """
) as dag:
    # Task 1: Initialize Staging Table
    create_staging_table = PythonOperator(
        task_id='create_staging_table',
        python_callable=_execute_sql_file,
        op_kwargs={
            'sql_file_path': '/opt/airflow/dags/sql/create_table_staging_raw_air_quality.sql',
            'conn_id': 'neon_db_conn' # Menggunakan ID koneksi yang akan kita buat di Airflow UI
        },
        doc_md="Membuat tabel staging `raw_air_quality` di Neon DB jika belum ada."
    )

    # Task 2: Initialize Warehouse Table
    create_warehouse_table = PythonOperator(
        task_id='create_warehouse_table',
        python_callable=_execute_sql_file,
        op_kwargs={
            'sql_file_path': '/opt/airflow/dags/sql/create_table_yearly_air_quality.sql',
            'conn_id': 'neon_db_conn' # Menggunakan ID koneksi yang akan kita buat di Airflow UI
        },
        doc_md="Membuat tabel warehouse `fact_yearly_air_quality` di Neon DB jika belum ada."
    )

    # Task 3: Extract Data from Local CSVs and Load to Staging
    extract_and_load_to_staging = BashOperator(
        task_id='extract_and_load_to_staging',
        bash_command=f'python /opt/airflow/dags/scripts/extract_local_csv.py "{NEON_DB_CONN_STRING}"',
        doc_md="Mengekstrak data dari file CSV lokal dan memuatnya ke tabel staging di Neon DB."
    )

    # Task 4: Run Spark Job for Transformation and Load to Warehouse
    # Pastikan Spark Master dapat dijangkau dari kontainer Airflow Worker/Scheduler
    run_spark_transformation = BashOperator(
        task_id='run_spark_transformation',
        bash_command='spark-submit --master spark://spark_master:7077 ' \
                     '--packages org.postgresql:postgresql:42.6.0 ' \
                     '/opt/airflow/spark_jobs/yearly_air_quality.py ' \
                     f'"{NEON_DB_CONN_STRING}"',
        doc_md="Menjalankan job Apache Spark untuk transformasi data dan memuatnya ke tabel warehouse."
    )

    # Define task dependencies
    create_staging_table >> create_warehouse_table >> extract_and_load_to_staging >> run_spark_transformation
