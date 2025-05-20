# Analisis-Konsumsi-Listrik-Klasterisasi-Wilayah-Berdasarkan-Tingkat-Aktivitas-di-Sumatera

## 🧠 Deskripsi Singkat

Proyek ini merupakan implementasi sistem Big Data berbasis Hadoop Ecosystem untuk menganalisis konsumsi listrik dari smart meter di wilayah Sumatera. Sistem ini menggunakan arsitektur *Medallion* (Bronze–Silver–Gold) untuk menyimpan dan memproses data dalam tiga lapisan: data mentah, data yang telah dibersihkan, dan data hasil agregasi serta analitik. Pipeline ETL dikembangkan menggunakan Apache Spark untuk transformasi dan klasterisasi wilayah berdasarkan pola konsumsi listrik harian dan mingguan dengan algoritma K-Means dari Spark MLlib. Data juga diperkaya dengan informasi cuaca dan demografi untuk memberikan konteks analitik yang lebih luas. Hasil akhirnya divisualisasikan dalam bentuk dashboard interaktif menggunakan Apache Superset guna mendukung pengambilan keputusan berbasis data dalam sektor energi.

___
## 🏗️ Arsitektur Sistem

Bronze Layer: Menyimpan data mentah dari smart meter, cuaca, dan demografi.

Silver Layer: Data dibersihkan dan ditransformasi.

Gold Layer: Data agregasi dan hasil klasterisasi disimpan untuk analisis.

___
## 🔧 Tools


___
## 🧩Struktur Folder


___


