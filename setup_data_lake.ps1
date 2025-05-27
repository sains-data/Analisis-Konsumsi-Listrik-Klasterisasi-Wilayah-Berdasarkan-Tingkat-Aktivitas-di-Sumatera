# Electricity Data Lake Setup Script
# This script initializes the HDFS directories and Hive databases

Write-Host "🚀 Setting up Electricity Data Lake..." -ForegroundColor Green

# Wait for services to be ready
Write-Host "⏳ Waiting for Hadoop services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Create HDFS directories
Write-Host "📁 Creating HDFS directory structure..." -ForegroundColor Blue
docker exec namenode hdfs dfs -mkdir -p /electricity
docker exec namenode hdfs dfs -mkdir -p /electricity/bronze
docker exec namenode hdfs dfs -mkdir -p /electricity/silver
docker exec namenode hdfs dfs -mkdir -p /electricity/gold
docker exec namenode hdfs dfs -mkdir -p /user/hive/warehouse

# Set permissions
Write-Host "🔐 Setting HDFS permissions..." -ForegroundColor Blue
docker exec namenode hdfs dfs -chmod -R 777 /electricity
docker exec namenode hdfs dfs -chmod -R 777 /user/hive/warehouse

# Copy initial data to HDFS if exists
Write-Host "📤 Uploading initial data to HDFS..." -ForegroundColor Blue
if (Test-Path "bronze\data_listrik_raw.csv") {
    docker exec namenode hdfs dfs -put /data/bronze/data_listrik_raw.csv /electricity/bronze/
    Write-Host "✅ Data uploaded successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️ No initial data found in bronze folder" -ForegroundColor Yellow
}

# Create Hive databases
Write-Host "🗄️ Creating Hive databases..." -ForegroundColor Blue
$hiveCommands = @"
CREATE DATABASE IF NOT EXISTS electricity_bronze;
CREATE DATABASE IF NOT EXISTS electricity_silver;
CREATE DATABASE IF NOT EXISTS electricity_gold;
SHOW DATABASES;
"@

docker exec hive-server beeline -u "jdbc:hive2://localhost:10000" -e $hiveCommands

Write-Host "✅ Data Lake setup completed!" -ForegroundColor Green

# Show HDFS structure
Write-Host "📋 HDFS Structure:" -ForegroundColor Cyan
docker exec namenode hdfs dfs -ls -R /electricity

Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Access URLs:" -ForegroundColor Cyan
Write-Host "- HDFS NameNode: http://localhost:9870" -ForegroundColor White
Write-Host "- Spark Master: http://localhost:8080" -ForegroundColor White
Write-Host "- Hive Server: jdbc:hive2://localhost:10000" -ForegroundColor White
Write-Host "- Jupyter Lab: http://localhost:8888 (token: electricity123)" -ForegroundColor White
Write-Host "- Superset: http://localhost:8088 (admin/admin)" -ForegroundColor White
Write-Host "- MinIO Console: http://localhost:9001 (minioadmin/minioadmin123)" -ForegroundColor White
