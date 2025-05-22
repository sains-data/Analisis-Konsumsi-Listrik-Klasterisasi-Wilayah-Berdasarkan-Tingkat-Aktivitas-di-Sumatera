# Analisis-Konsumsi-Listrik-Klasterisasi-Wilayah-Berdasarkan-Tingkat-Aktivitas-di-Sumatera

## 🧠 Deskripsi Singkat

Proyek ini merupakan implementasi sistem Big Data berbasis Hadoop Ecosystem untuk menganalisis konsumsi listrik dari smart meter di wilayah Sumatera. Sistem ini menggunakan arsitektur *Medallion* (Bronze–Silver–Gold) untuk menyimpan dan memproses data dalam tiga lapisan: data mentah, data yang telah dibersihkan, dan data hasil agregasi serta analitik. Pipeline ETL dikembangkan menggunakan Apache Spark untuk transformasi dan klasterisasi wilayah berdasarkan pola konsumsi listrik harian dan mingguan dengan algoritma K-Means dari Spark MLlib. Data juga diperkaya dengan informasi cuaca dan demografi untuk memberikan konteks analitik yang lebih luas. Hasil akhirnya divisualisasikan dalam bentuk dashboard interaktif menggunakan Apache Superset guna mendukung pengambilan keputusan berbasis data dalam sektor energi.

___
## 🏗️ Arsitektur Sistem

Proyek ini mengadopsi arsitektur **Medallion Architecture (Bronze – Silver – Gold)** dan menggunakan berbagai komponen dalam ekosistem Apache Hadoop. Alur sistem dirancang untuk melakukan ingestion, pembersihan, transformasi, klasterisasi, dan visualisasi data secara batch.
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
  
___
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
## 🧩Struktur Folder HDFS
Representasi dari organisasi data di dalam cluster Hadoop, mengikuti **Medallion Architecture** (Bronze, Silver, Gold Layers). Ini memastikan data disimpan secara terstruktur pada setiap tahap transformasi.

| Layer                               | Path HDFS                           | Format               | Tujuan                                                                                     |
| :---------------------------------- | :---------------------------------- | :------------------- | :----------------------------------------------------------------------------------------- |
| **Bronze Layer** (Raw Data)         | `/data/bronze/` | CSV, JSON     | Arsip permanen data mentah dari sumber eksternal tanpa perubahan.                  |
| **Silver Layer** (Cleaned Data)     | `/data/silver/` | Parquet    | Data terstruktur, bersih, dan efisien dalam penyimpanan, siap dianalisis.        |
| **Gold Layer** (Analytics-Ready)    | `/data/gold/`  | Parquet, ORC | Untuk kebutuhan laporan, query cepat, dan visualisasi ke end-user. |
| **Temp Layer** (Temporary files)    | `/data/tmp/`   | (N/A)                | Digunakan untuk file sementara selama proses ETL.                    |

___
## 📂 Dataset
### 1. Atribut Data Konsumsi Listrik (Data Smart Meter)

Data ini merupakan inti dari analisis, memberikan detail penggunaan listrik dari setiap smart meter. 

| Atribut             | Tipe Data  | Deskripsi                                                                 |
| :------------------ | :--------- | :------------------------------------------------------------------------ |
| `timestamp`         | `datetime` | Waktu pengambilan data (biasanya dalam interval per 15 menit atau per jam). |
| `meter_id`          | `string`   | ID unik untuk setiap smart meter.                                   |
| `region`            | `string`   | Wilayah (misalnya: Kota, Kabupaten, Provinsi di Sumatera).    |
| `voltage`           | `float`    | Tegangan listrik dalam volt.                                 |
| `current`           | `float`    | Arus listrik dalam ampere.                                   |
| `power_consumption` | `float`    | Konsumsi daya aktif (kWh) selama interval waktu tersebut.      |
| `power_factor`      | `float`    | Faktor daya (antara 0 dan 1).                                 |
| `outage_flag`       | `boolean`  | Apakah ada pemadaman listrik saat itu (True atau False).      |

### 2. Atribut Data Cuaca (BMKG API/Simulasi)

Informasi cuaca digunakan untuk menganalisis korelasinya dengan pola konsumsi listrik.

| Atribut             | Tipe Data | Deskripsi                               |
| :------------------ | :-------- | :-------------------------------------- |
| `temperature`       | `float`   | Suhu udara (°C).             |
| `humidity`          | `float`   | Kelembaban relatif (%).     |
| `rainfall`          | `float`   | Curah hujan (mm).           |
| `weather_condition` | `string`  | Deskripsi cuaca (contoh: "Hujan ringan", "Berawan", "Cerah"). |
| `wind_speed`        | `float`   | Kecepatan angin ($km/jam$). |

### 3. Atribut Data Demografi & Sosial Ekonomi (BPS)

Data demografi dan sosial ekonomi memberikan konteks tambahan untuk memahami karakteristik wilayah.

| Atribut              | Tipe Data | Deskripsi                               |
| :------------------- | :-------- | :-------------------------------------- |
| `population_density` | `float`   | Kepadatan penduduk $(jiwa/km^{2})$. |
| `urbanization_level` | `string`  | Tingkat urbanisasi (contoh: "Perkotaan", "Pedesaan"). |
| `average_income`     | `float`   | Pendapatan rata-rata per kapita (Rp). |
| `economic_activity`  | `string`  | Dominasi sektor ekonomi (contoh: "Industri", "Pertanian", "Jasa"). |
| `household_size`     | `float`   | Rata-rata jumlah anggota rumah tangga. |

### 4. Format Penyimpanan Data di HDFS

Data akan disimpan dalam format yang berbeda di setiap lapisan Medallion Architecture di HDFS untuk optimasi dan efisiensi.

* **Bronze Layer**: (Raw) CSV/JSON di `/data/bronze/konsumsi/2025-01.csv`
* **Silver Layer**: (Cleaned) Parquet di `/data/silver/konsumsi/2025.parquet`
* **Gold Layer**: (Aggregated) ORC/Parquet di `/data/gold/klasterisasi/summary_cluster.parquet`

___
## ⚙️ Proses ETL
## Proses ETL (Extract, Transform, Load)

Proses ETL adalah tulang punggung dari pipeline data ini, memastikan data mengalir secara efisien dan transformatif dari sumber mentah hingga menjadi informasi yang siap untuk analitik. Proses ini dirancang untuk berjalan secara *batch processing* menggunakan Apache Spark sebagai *engine* utamanya.

### 1. Extract (Bronze Layer)

Tahap ini bertanggung jawab untuk pengambilan data dari berbagai sumber dan menyimpannya di lapisan Bronze (Raw Data) HDFS tanpa modifikasi.

* **Aktivitas**: Mengambil data dari smart meter (simulasi), API BMKG (data cuaca), dan data demografi (BPS).
* **Tools**: Bash scripting (`curl`) dan HDFS CLI untuk mengunggah data.
* **Output**: Data mentah disimpan dalam format CSV atau JSON di HDFS pada path `/data/bronze/`. Contoh: `/data/bronze/konsumsi/2025-01.csv`.

### 2. Transform (Silver Layer)

Tahap ini fokus pada pembersihan, validasi, dan transformasi data untuk meningkatkan kualitas dan efisiensi.

* **Aktivitas**:
    * Validasi skema data.
    * Pembersihan nilai `null` atau tidak valid.
    * Penanganan duplikasi data.
    * Parsing `datetime` ke format standar.
    * Normalisasi kolom numerik (opsional).
    * *Feature engineering* untuk membuat fitur baru yang relevan (misalnya agregasi harian, variasi waktu).
    * Integrasi (join) antar-sumber data (smart meter, cuaca, demografi).
* **Tools**: Apache Spark, Hive Metastore.
* **Output**: Data bersih dan terstruktur disimpan dalam format Parquet di HDFS pada path `/data/silver/`. Contoh: `/data/silver/konsumsi/2025.parquet`.

### 3. Load (Gold Layer)

Tahap terakhir ini memuat data yang sudah siap analitik dan mengaplikasikan algoritma klasterisasi.

* **Aktivitas**:
    * Menghitung metrik agregat seperti total konsumsi per wilayah per hari.
    * Menerapkan algoritma klasterisasi **K-Means** menggunakan Spark MLlib untuk mengelompokkan wilayah berdasarkan pola konsumsi listrik.
    * Menyimpan hasil klasterisasi dan ringkasan agregat.
    * Mendaftarkan data Gold Layer sebagai tabel di Apache Hive untuk memudahkan query dan akses visualisasi.
* **Tools**: Spark MLlib, Spark SQL, HDFS, Apache Hive.
* **Output**: Data hasil analisis akhir disimpan dalam format kolumnar efisien (Parquet/ORC) di HDFS pada path `/data/gold/`. Contoh: `/data/gold/klasterisasi/summary_cluster.parquet`. Model klasterisasi juga disimpan di `/models/kmeans_cluster/`.

___
## 🔍 Analisis & ML


___
## 📊 Visualisasi


___
## 🧪 Pengujian


___
## 🚀 Deployment


