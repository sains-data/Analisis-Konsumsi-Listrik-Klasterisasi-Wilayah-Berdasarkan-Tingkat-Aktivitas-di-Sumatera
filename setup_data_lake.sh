#!/bin/bash

# Electricity Data Lake Setup Script
# This script initializes the HDFS directories and Hive databases

echo "🚀 Setting up Electricity Data Lake..."

# Wait for services to be ready
echo "⏳ Waiting for Hadoop services to be ready..."
sleep 30

# Create HDFS directories
echo "📁 Creating HDFS directory structure..."
docker exec namenode hdfs dfs -mkdir -p /electricity
docker exec namenode hdfs dfs -mkdir -p /electricity/bronze
docker exec namenode hdfs dfs -mkdir -p /electricity/silver
docker exec namenode hdfs dfs -mkdir -p /electricity/gold
docker exec namenode hdfs dfs -mkdir -p /user/hive/warehouse

# Set permissions
echo "🔐 Setting HDFS permissions..."
docker exec namenode hdfs dfs -chmod -R 777 /electricity
docker exec namenode hdfs dfs -chmod -R 777 /user/hive/warehouse

# Copy initial data to HDFS
echo "📤 Uploading initial data to HDFS..."
docker exec namenode hdfs dfs -put /data/bronze/data_listrik_raw.csv /electricity/bronze/

# Create Hive databases
echo "🗄️ Creating Hive databases..."
docker exec hive-server beeline -u jdbc:hive2://localhost:10000 -e "
CREATE DATABASE IF NOT EXISTS electricity_bronze;
CREATE DATABASE IF NOT EXISTS electricity_silver;
CREATE DATABASE IF NOT EXISTS electricity_gold;
SHOW DATABASES;
"

echo "✅ Data Lake setup completed!"

# Show HDFS structure
echo "📋 HDFS Structure:"
docker exec namenode hdfs dfs -ls -R /electricity

echo "🎉 Setup completed successfully!"
echo ""
echo "Access URLs:"
echo "- HDFS NameNode: http://localhost:9870"
echo "- Spark Master: http://localhost:8080"
echo "- Hive Server: jdbc:hive2://localhost:10000"
echo "- Jupyter Lab: http://localhost:8888 (token: electricity123)"
echo "- Superset: http://localhost:8088 (admin/admin)"
echo "- MinIO Console: http://localhost:9001 (minioadmin/minioadmin123)"
