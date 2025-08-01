
CREATE SCHEMA IF NOT EXISTS staging;


CREATE TABLE IF NOT EXISTS staging.raw_air_quality (
    tahun INTEGER,
    kota VARCHAR(255),
    parameter VARCHAR(255),
    nilai NUMERIC,
    satuan VARCHAR(50),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


COMMENT ON TABLE staging.raw_air_quality IS 'Tabel staging untuk data kualitas udara mentah dari berbagai sumber.';
COMMENT ON COLUMN staging.raw_air_quality.tahun IS 'Tahun pengukuran kualitas udara.';
COMMENT ON COLUMN staging.raw_air_quality.kota IS 'Nama kota tempat pengukuran dilakukan.';
COMMENT ON COLUMN staging.raw_air_quality.parameter IS 'Parameter polutan yang diukur (misalnya, PM2.5).';
COMMENT ON COLUMN staging.raw_air_quality.nilai IS 'Nilai konsentrasi polutan.';
COMMENT ON COLUMN staging.raw_air_quality.satuan IS 'Satuan pengukuran polutan.';
COMMENT ON COLUMN staging.raw_air_quality.load_timestamp IS 'Timestamp saat data dimuat ke tabel staging.';
