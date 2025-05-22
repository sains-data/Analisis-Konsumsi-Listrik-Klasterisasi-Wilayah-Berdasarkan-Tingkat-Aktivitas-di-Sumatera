# Analisis-Konsumsi-Listrik-Klasterisasi-Wilayah-Berdasarkan-Tingkat-Aktivitas-di-Sumatera

## 🧠 Deskripsi Singkat

Proyek ini merupakan implementasi sistem Big Data berbasis Hadoop Ecosystem untuk menganalisis konsumsi listrik dari smart meter di wilayah Sumatera. Sistem ini menggunakan arsitektur *Medallion* (Bronze–Silver–Gold) untuk menyimpan dan memproses data dalam tiga lapisan: data mentah, data yang telah dibersihkan, dan data hasil agregasi serta analitik. Pipeline ETL dikembangkan menggunakan Apache Spark untuk transformasi dan klasterisasi wilayah berdasarkan pola konsumsi listrik harian dan mingguan dengan algoritma K-Means dari Spark MLlib. Data juga diperkaya dengan informasi cuaca dan demografi untuk memberikan konteks analitik yang lebih luas. Hasil akhirnya divisualisasikan dalam bentuk dashboard interaktif menggunakan Apache Superset guna mendukung pengambilan keputusan berbasis data dalam sektor energi.

___
## 🏗️ Arsitektur Sistem

Proyek ini mengadopsi arsitektur **Medallion Architecture (Bronze – Silver – Gold)** dan menggunakan berbagai komponen dalam ekosistem Apache Hadoop. Alur sistem dirancang untuk melakukan ingestion, pembersihan, transformasi, klasterisasi, dan visualisasi data secara batch
<img src="https://github.com/user-attachments/assets/b34ae450-82c1-4fbf-84b6-2a44837cab26" alt="description of image">

### 🔰 Bronze Layer (Raw Data)
- **Sumber data:** Smart Meter, API Cuaca (BMKG), dan data Demografi (BPS).
- **Teknologi:** Bash, `curl`, HDFS.
- **Output:** File CSV/JSON disimpan ke HDFS (`/data/bronze/`).

### 🧼 Silver Layer (Cleaned Data)
- **Proses:** Validasi, pembersihan (drop null, parsing waktu), dan transformasi.
- **Teknologi:** Apache Spark, Hive Metastore.
- **Output:** Format Parquet di HDFS (`/data/silver/`).

### 💎 Gold Layer (Analytics Ready)
- **Proses:** Agregasi konsumsi listrik & klasterisasi wilayah dengan K-Means.
- **Teknologi:** Spark MLlib, Apache Hive, Apache Superset.
- **Output:** Tabel analitik di Hive (`/data/gold/`), visualisasi interaktif.

### ⚙️ Orkestrasi & Monitoring
- **Apache Airflow:** Menjadwalkan dan menjalankan pipeline ingestion hingga analitik.
- **Apache Ambari:** Monitoring performa cluster Hadoop dan job Spark.

### 🔄 Alur Data Sistem

1. **Ambil Data (Bronze):**  
   Smart Meter dan cuaca dikumpulkan secara berkala ke `/data/bronze`.

2. **Pembersihan & Transformasi (Silver):**  
   Data mentah dibersihkan dan diubah ke format Parquet yang efisien di `/data/silver`.

3. **Agregasi & Analitik (Gold):**  
   Data diklasterisasi berdasarkan pola konsumsi dan disimpan untuk analisis di `/data/gold`.

4. **Visualisasi:**  
   Dashboard interaktif dibuat menggunakan Apache Superset yang terhubung ke Hive.

### 🧱 Komponen Utama

| Komponen        | Fungsi                                                                 |
|----------------|------------------------------------------------------------------------|
| **Hadoop HDFS** | Penyimpanan data mentah dan hasil ETL secara terdistribusi             |
| **Apache Spark**| Transformasi data, feature engineering, klasterisasi (MLlib)           |
| **Apache Hive** | Query SQL-like dan metadata management untuk data analitik             |
| **Superset**    | Visualisasi dashboard interaktif                                        |
| **Airflow**     | Penjadwalan pipeline ETL                                                |
| **Ambari**      | Monitoring cluster Hadoop                                               |
| **Docker**      | Menyediakan lingkungan terkontainerisasi untuk seluruh komponen        |
___
## 🔧 Tools


| No. | Tools / Teknologi   | Kategori              | Fungsi Utama                                                                 |
|-----|----------------------|------------------------|------------------------------------------------------------------------------|
| 1   | **Hadoop HDFS**      | Storage                | Penyimpanan data mentah, hasil transformasi, dan agregasi secara terdistribusi |
| 2   | **Apache Spark**     | ETL & Analytics        | Membersihkan data, transformasi, feature engineering, clustering & agregasi |
| 3   | **Apache Hive**      | Query Engine & Metadata| SQL query untuk data Gold Layer & metadata manajemen                        |
| 4   | **Apache Superset**  | Visualisasi            | Menyajikan dashboard klasterisasi dan tren konsumsi listrik                 |
| 5   | **Apache Airflow**   | Workflow Orchestration | Menjadwalkan pipeline batch secara otomatis dengan DAG                      |
| 6   | **Apache Ambari**    | Cluster Management     | Monitoring performa cluster Hadoop dan status service                       |
| 7   | **Docker**           | Deployment             | Virtualisasi layanan Hadoop & lingkungan multi-container                    |
| 8   | **Docker Compose**   | Deployment             | Menjalankan semua kontainer Hadoop ecosystem secara bersamaan              |
| 9   | **Bash + Crontab**   | Scheduler & Scripting  | Menjadwalkan ingestion data dari API                                        |
| 10  | **Jupyter Notebook** | Testing & Validation   | Validasi manual output Spark dan eksplorasi data                            |
| 11  | **Hive CLI**         | Query Interface        | Menjalankan query HiveQL dari terminal                                      |

___
## 🧩Struktur Folder


___
## 📂 Dataset


___
## ⚙️ Proses ETL


___
## 🔍 Analisis & ML


___
## 📊 Visualisasi


___
## 🧪 Pengujian


___
## 🚀 Deployment


