# Analisis Konsumsi Listrik & Klasterisasi Wilayah Berdasarkan Aktivitas di Sumatera

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com/)
[![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.3.0-orange.svg)](https://spark.apache.org/)
[![Apache Hadoop](https://img.shields.io/badge/Apache%20Hadoop-3.2.1-yellow.svg)](https://hadoop.apache.org/)

## 📋 Deskripsi Proyek

Proyek ini menganalisis konsumsi listrik dan mengklasterisasi wilayah di Sumatera berdasarkan tingkat aktivitas menggunakan arsitektur data lake modern (Bronze-Silver-Gold) dengan teknologi big data seperti HDFS, Hive, Spark, dan Superset.

### 📊 Fitur Analisis

- **Analisis Konsumsi Regional**: Mengidentifikasi pola konsumsi listrik di berbagai wilayah Sumatera
- **Klasterisasi Wilayah**: Mengelompokkan wilayah berdasarkan pola konsumsi dan karakteristik demografi
- **Analisis Temporal**: Pola konsumsi harian, mingguan, dan musiman
- **Korelasi Cuaca**: Menganalisis dampak suhu, curah hujan, dan faktor cuaca lainnya
- **Deteksi Anomali**: Mengidentifikasi pola tidak normal dalam konsumsi

## 🏗️ Arsitektur

Proyek ini mengimplementasikan arsitektur **Medalion (Bronze-Silver-Gold)** untuk data lake:

![Architecture Diagram](https://miro.medium.com/v2/resize:fit:1400/1*MoqE1BTBku4_XRwlLpQw6A.png)

### Bronze Layer (Raw Data)
- **Lokasi**: `hdfs://namenode:9000/electricity/bronze/`
- **Format**: CSV/Parquet
- **Isi**: Data mentah konsumsi listrik
- **Tabel Hive**: `electricity_bronze.raw_data`

### Silver Layer (Cleaned Data)
- **Lokasi**: `hdfs://namenode:9000/electricity/silver/`
- **Format**: Parquet (partitioned by year/month)
- **Isi**: Data yang sudah dibersihkan dan divalidasi
- **Tabel Hive**: `electricity_silver.cleaned_data`

### Gold Layer (Aggregated Data)
- **Lokasi**: `hdfs://namenode:9000/electricity/gold/`
- **Format**: Parquet
- **Isi**: Data yang siap untuk analisis bisnis
- **Tabel Hive**:
  - `electricity_gold.monthly_consumption`
  - `electricity_gold.daily_consumption`
  - `electricity_gold.hourly_patterns`

## 🚀 Teknologi yang Digunakan

- **Storage**: HDFS, MinIO (S3-compatible)
- **Processing**: Apache Spark (PySpark)
- **Metadata**: Apache Hive
- **Orchestration**: Docker Compose
- **Analytics**: Jupyter Notebooks
- **Visualization**: Apache Superset
- **Monitoring**: Prometheus + Grafana
- **Language**: Python 3.10+

## 🛠️ Memulai

### Prasyarat

- Docker dan Docker Compose
- Minimal 8GB RAM dan 20GB disk space

### Instalasi dan Menjalankan

1. **Clone repository**:
   ```bash
   git clone https://github.com/sains-data/Analisis-Konsumsi-Listrik-Klasterisasi-Wilayah-Berdasarkan-Tingkat-Aktivitas-di-Sumatera.git
   cd Analisis-Konsumsi-Listrik-Klasterisasi-Wilayah-Berdasarkan-Tingkat-Aktivitas-di-Sumatera
   ```

2. **Jalankan infrastruktur**:
   ```bash
   docker-compose up -d
   ```

3. **Setup data lake**:
   - Windows: `.\setup_data_lake.ps1`
   - Linux/Mac: `./setup_data_lake.sh`

4. **Jalankan ETL pipeline**:
   ```bash
   docker exec spark-master spark-submit \
     --master spark://spark-master:7077 \
     --deploy-mode client \
     /opt/workspace/notebooks/electricity_etl_spark.py
   ```

### Akses Layanan

| Layanan | URL | Kredensial |
|---------|-----|------------|
| **HDFS NameNode** | http://localhost:9870 | - |
| **Spark Master** | http://localhost:8080 | - |
| **Jupyter Lab** | http://localhost:8888 | Token: `electricity123` |
| **Superset** | http://localhost:8088 | admin/admin |
| **MinIO Console** | http://localhost:9001 | minioadmin/minioadmin123 |

## 📊 Analisis & Visualisasi

### Studi Kasus yang Tersedia

1. **Pola Konsumsi Regional**
   - Perbandingan konsumsi listrik antar wilayah di Sumatera
   - Klasterisasi wilayah berdasarkan karakteristik konsumsi

2. **Analisis Temporal**
   - Pola konsumsi berdasarkan waktu (jam, hari, bulan)
   - Peak hour detection dan load balancing

3. **Korelasi dengan Faktor Eksternal**
   - Hubungan antara konsumsi listrik dengan suhu, curah hujan
   - Dampak urbanisasi dan aktivitas ekonomi

### Dashboard Superset

1. **Regional Dashboard**
   ![Sample Dashboard](https://kinsta.com/wp-content/uploads/2023/02/apache-superset-dashboard.jpg)

2. **Temporal Analysis**
   ![Sample Dashboard](https://superset.apache.org/img/time-dash.jpg)

## 🧪 Dataset

Dataset berisi data konsumsi listrik sintesis yang mencakup:

- Timestamp
- Meter ID
- Region (Wilayah di Sumatera)
- Voltage, Current, Power Consumption
- Temperature, Humidity, Rainfall
- Urbanization Level
- Economic Activity

## 👥 Kontributor

- [Your Name](https://github.com/yourusername)
- [Team Member](https://github.com/teammember)

## 📄 Lisensi

Project ini dilisensikan di bawah [MIT License](LICENSE).
