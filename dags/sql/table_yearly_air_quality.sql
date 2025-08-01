-- Pastikan skema 'warehouse' ada
CREATE SCHEMA IF NOT EXISTS warehouse;

-- Buat tabel fact_yearly_air_quality di skema warehouse
-- Tabel ini akan dipartisi berdasarkan tahun
CREATE TABLE IF NOT EXISTS warehouse.fact_yearly_air_quality (
    tahun INTEGER NOT NULL,
    kota VARCHAR(255) NOT NULL,
    parameter VARCHAR(255) NOT NULL,
    avg_nilai NUMERIC,
    max_nilai NUMERIC,
    min_nilai NUMERIC,
    satuan VARCHAR(50),
    processed_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) PARTITION BY RANGE (tahun);

-- Buat partisi untuk tahun-tahun yang relevan
-- Kamu bisa menambahkan lebih banyak partisi di sini atau secara dinamis
CREATE TABLE IF NOT EXISTS warehouse.fact_yearly_air_quality_y2022 PARTITION OF warehouse.fact_yearly_air_quality
    FOR VALUES FROM (2022) TO (2023);

CREATE TABLE IF NOT EXISTS warehouse.fact_yearly_air_quality_y2023 PARTITION OF warehouse.fact_yearly_air_quality
    FOR VALUES FROM (2023) TO (2024);

CREATE TABLE IF NOT EXISTS warehouse.fact_yearly_air_quality_y2024 PARTITION OF warehouse.fact_yearly_air_quality
    FOR VALUES FROM (2024) TO (2025);

CREATE TABLE IF NOT EXISTS warehouse.fact_yearly_air_quality_y2025 PARTITION OF warehouse.fact_yearly_air_quality
    FOR VALUES FROM (2025) TO (2026);

-- Tambahkan komentar untuk dokumentasi
COMMENT ON TABLE warehouse.fact_yearly_air_quality IS 'Tabel fakta untuk data kualitas udara tahunan yang sudah diagregasi dan siap analisis.';
COMMENT ON COLUMN staging.raw_air_quality.tahun IS 'Tahun pengukuran kualitas udara.';
COMMENT ON COLUMN staging.raw_air_quality.kota IS 'Nama kota tempat pengukuran dilakukan.';
COMMENT ON COLUMN staging.raw_air_quality.parameter IS 'Parameter polutan yang diukur (misalnya, PM2.5).';
COMMENT ON COLUMN staging.raw_air_quality.avg_nilai IS 'Nilai rata-rata polutan untuk tahun tersebut.';
COMMENT ON COLUMN staging.raw_air_quality.max_nilai IS 'Nilai maksimum polutan untuk tahun tersebut.';
COMMENT ON COLUMN staging.raw_air_quality.min_nilai IS 'Nilai minimum polutan untuk tahun tersebut.';
COMMENT ON COLUMN staging.raw_air_quality.satuan IS 'Satuan pengukuran polutan.';
COMMENT ON COLUMN staging.raw_air_quality.processed_timestamp IS 'Timestamp saat data diproses dan dimuat ke tabel warehouse.';
