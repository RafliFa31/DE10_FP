import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, min, current_timestamp
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, DecimalType
from urllib.parse import urlparse

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

def run_spark_job(neon_db_conn_string):
    """
    Menjalankan job Spark untuk transformasi dan agregasi data kualitas udara.
    """
    print("Starting Spark job for air quality data transformation...")

    # Ekstrak detail DB
    db_details = get_db_details_from_conn_string(neon_db_conn_string)

    spark = SparkSession.builder \
        .appName("YearlyAirQualityTransformation") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
        .config("spark.driver.extraClassPath", "/opt/spark/jars/postgresql-42.6.0.jar") \
        .config("spark.executor.extraClassPath", "/opt/spark/jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    # Skema untuk data staging
    staging_schema = StructType([
        StructField("tahun", IntegerType(), True),
        StructField("kota", StringType(), True),
        StructField("parameter", StringType(), True),
        StructField("nilai", DoubleType(), True), # Gunakan DoubleType untuk nilai numerik
        StructField("satuan", StringType(), True),
        StructField("load_timestamp", StringType(), True) # Akan dibaca sebagai string, tidak digunakan dalam transformasi ini
    ])

    # Baca data dari tabel staging di Neon DB
    try:
        df_raw = spark.read \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{db_details['host']}:{db_details['port']}/{db_details['database']}") \
            .option("dbtable", "staging.raw_air_quality") \
            .option("user", db_details['user']) \
            .option("password", db_details['password']) \
            .option("sslmode", db_details['sslmode']) \
            .load()
        print("Data read from staging.raw_air_quality:")
        df_raw.printSchema()
        df_raw.show(5)
    except Exception as e:
        print(f"Error reading from staging table: {e}")
        spark.stop()
        sys.exit(1)

    if df_raw.count() == 0:
        print("Staging table is empty. No data to process.")
        spark.stop()
        return

    # Transformasi dan Agregasi
    # Filter hanya untuk PM2.5 dan Bandung (sesuai fokus proyek)
    df_filtered = df_raw.filter((col("parameter") == "pm2.5") & (col("kota") == "Bandung"))

    # Agregasi data per tahun, kota, parameter
    df_aggregated = df_filtered.groupBy("tahun", "kota", "parameter") \
                               .agg(
                                   avg(col("nilai")).alias("avg_nilai"),
                                   max(col("nilai")).alias("max_nilai"),
                                   min(col("nilai")).alias("min_nilai")
                               ) \
                               .withColumn("satuan", col("satuan")) \
                               .withColumn("processed_timestamp", current_timestamp())

    print("Aggregated data schema:")
    df_aggregated.printSchema()
    print("Aggregated data preview:")
    df_aggregated.show()

    # Tulis data yang sudah diagregasi ke tabel warehouse
    try:
        df_aggregated.write \
            .format("jdbc") \
            .option("url", f"jdbc:postgresql://{db_details['host']}:{db_details['port']}/{db_details['database']}") \
            .option("dbtable", "warehouse.fact_yearly_air_quality") \
            .option("user", db_details['user']) \
            .option("password", db_details['password']) \
            .option("sslmode", db_details['sslmode']) \
            .mode("append") # Gunakan append karena tabel dipartisi
            
        .save()
        print("Successfully loaded aggregated data to warehouse.fact_yearly_air_quality.")
    except Exception as e:
        print(f"Error writing to warehouse table: {e}")
        spark.stop()
        sys.exit(1)

    spark.stop()
    print("Spark job finished.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: spark-submit yearly_air_quality.py <NEON_DB_CONN_STRING>")
        sys.exit(1)
    neon_db_conn_string = sys.argv[1]
    run_spark_job(neon_db_conn_string)

