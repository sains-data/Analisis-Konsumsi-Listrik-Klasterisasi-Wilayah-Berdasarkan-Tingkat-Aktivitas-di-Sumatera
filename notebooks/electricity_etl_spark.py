#!/usr/bin/env python3
"""
ETL Pipeline untuk Data Listrik menggunakan PySpark
Bronze -> Silver -> Gold Layer dengan HDFS dan Hive
"""

import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ElectricityETL:
    def __init__(self):
        """Initialize Spark session dengan konfigurasi untuk HDFS dan Hive"""
        self.spark = SparkSession.builder \
            .appName("ElectricityDataETL") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
            .config("spark.sql.warehouse.dir", "hdfs://namenode:9000/user/hive/warehouse") \
            .config("spark.hadoop.javax.jdo.option.ConnectionURL", 
                   "jdbc:postgresql://hive-metastore-postgresql:5432/metastore") \
            .config("spark.hadoop.javax.jdo.option.ConnectionUserName", "hive") \
            .config("spark.hadoop.javax.jdo.option.ConnectionPassword", "hive") \
            .enableHiveSupport() \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        logger.info("Spark session initialized successfully")

    def create_bronze_layer(self, input_path="bronze/data_listrik_raw.csv"):
        """
        Bronze Layer: Raw data ingestion ke HDFS
        """
        logger.info("Starting Bronze layer processing...")
        
        # Define schema untuk data listrik
        schema = StructType([
            StructField("timestamp", TimestampType(), True),
            StructField("meter_id", StringType(), True),
            StructField("region", StringType(), True),
            StructField("voltage", DoubleType(), True),
            StructField("current", DoubleType(), True),
            StructField("power_consumption", DoubleType(), True),
            StructField("power_factor", DoubleType(), True),
            StructField("outage_flag", BooleanType(), True),
            StructField("temperature", DoubleType(), True),
            StructField("humidity", DoubleType(), True),
            StructField("rainfall", DoubleType(), True),
            StructField("weather_condition", StringType(), True),
            StructField("wind_speed", DoubleType(), True),
            StructField("population_density", DoubleType(), True),
            StructField("urbanization_level", StringType(), True),
            StructField("average_income", DoubleType(), True),
            StructField("economic_activity", StringType(), True),
            StructField("household_size", DoubleType(), True)
        ])
        
        # Read CSV data
        df_bronze = self.spark.read \
            .option("header", "true") \
            .option("inferSchema", "false") \
            .schema(schema) \
            .csv(input_path)
        
        # Write ke HDFS Bronze layer
        bronze_path = "hdfs://namenode:9000/electricity/bronze/data_listrik_raw"
        df_bronze.write \
            .mode("overwrite") \
            .parquet(bronze_path)
        
        # Create Hive external table untuk Bronze
        self.spark.sql(f"""
            CREATE DATABASE IF NOT EXISTS electricity_bronze
        """)
        
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS electricity_bronze.raw_data (
                timestamp timestamp,
                meter_id string,
                region string,
                voltage double,
                current double,
                power_consumption double,
                power_factor double,
                outage_flag boolean,
                temperature double,
                humidity double,
                rainfall double,
                weather_condition string,
                wind_speed double,
                population_density double,
                urbanization_level string,
                average_income double,
                economic_activity string,
                household_size double
            )
            USING PARQUET
            LOCATION '{bronze_path}'
        """)
        
        logger.info(f"Bronze layer created successfully with {df_bronze.count()} records")
        return df_bronze

    def create_silver_layer(self):
        """
        Silver Layer: Data cleaning dan validation
        """
        logger.info("Starting Silver layer processing...")
        
        # Read from Bronze layer
        df_bronze = self.spark.table("electricity_bronze.raw_data")
        
        # Data cleaning operations
        df_silver = df_bronze \
            .filter(col("power_consumption").isNotNull()) \
            .filter(col("region").isNotNull()) \
            .filter(col("timestamp").isNotNull()) \
            .withColumn("voltage", 
                       when(col("voltage") < 180, 180)
                       .when(col("voltage") > 240, 240)
                       .otherwise(col("voltage"))) \
            .withColumn("power_factor",
                       when(col("power_factor") < 0, 0)
                       .when(col("power_factor") > 1, 1)
                       .otherwise(col("power_factor"))) \
            .withColumn("date", to_date(col("timestamp"))) \
            .withColumn("hour", hour(col("timestamp"))) \
            .withColumn("month", date_format(col("timestamp"), "yyyy-MM")) \
            .withColumn("year", year(col("timestamp"))) \
            .withColumn("power_consumption_kwh", col("power_consumption")) \
            .filter(col("power_consumption_kwh") > 0)
        
        # Write ke HDFS Silver layer
        silver_path = "hdfs://namenode:9000/electricity/silver/data_listrik_cleaned"
        df_silver.write \
            .mode("overwrite") \
            .partitionBy("year", "month") \
            .parquet(silver_path)
        
        # Create Hive external table untuk Silver
        self.spark.sql(f"""
            CREATE DATABASE IF NOT EXISTS electricity_silver
        """)
        
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS electricity_silver.cleaned_data (
                timestamp timestamp,
                meter_id string,
                region string,
                voltage double,
                current double,
                power_consumption double,
                power_factor double,
                outage_flag boolean,
                temperature double,
                humidity double,
                rainfall double,
                weather_condition string,
                wind_speed double,
                population_density double,
                urbanization_level string,
                average_income double,
                economic_activity string,
                household_size double,
                date date,
                hour int,
                power_consumption_kwh double
            )
            USING PARQUET
            PARTITIONED BY (year int, month string)
            LOCATION '{silver_path}'
        """)
        
        # Recover partitions
        self.spark.sql("MSCK REPAIR TABLE electricity_silver.cleaned_data")
        
        logger.info(f"Silver layer created successfully with {df_silver.count()} records")
        return df_silver

    def create_gold_layer(self):
        """
        Gold Layer: Aggregated data untuk analytics dan reporting
        """
        logger.info("Starting Gold layer processing...")
        
        # Read from Silver layer
        df_silver = self.spark.table("electricity_silver.cleaned_data")
        
        # Agregasi per region dan month
        df_gold_monthly = df_silver.groupBy("region", "month") \
            .agg(
                sum("power_consumption_kwh").alias("total_kwh"),
                avg("power_consumption_kwh").alias("avg_kwh"),
                avg("temperature").alias("avg_temp"),
                sum("rainfall").alias("total_rain"),
                sum(when(col("outage_flag") == True, 1).otherwise(0)).alias("total_outages"),
                count("*").alias("total_readings"),
                avg("voltage").alias("avg_voltage"),
                avg("current").alias("avg_current"),
                avg("power_factor").alias("avg_power_factor"),
                avg("humidity").alias("avg_humidity"),
                avg("wind_speed").alias("avg_wind_speed")
            )
        
        # Agregasi per region dan date (daily)
        df_gold_daily = df_silver.groupBy("region", "date") \
            .agg(
                sum("power_consumption_kwh").alias("daily_total_kwh"),
                avg("power_consumption_kwh").alias("daily_avg_kwh"),
                avg("temperature").alias("daily_avg_temp"),
                sum("rainfall").alias("daily_total_rain"),
                sum(when(col("outage_flag") == True, 1).otherwise(0)).alias("daily_total_outages"),
                count("*").alias("daily_total_readings")
            )
        
        # Agregasi per region dan hour (hourly patterns)
        df_gold_hourly = df_silver.groupBy("region", "hour") \
            .agg(
                avg("power_consumption_kwh").alias("hourly_avg_kwh"),
                count("*").alias("hourly_readings")
            )
        
        # Write ke HDFS Gold layer
        monthly_path = "hdfs://namenode:9000/electricity/gold/monthly_aggregated"
        daily_path = "hdfs://namenode:9000/electricity/gold/daily_aggregated"
        hourly_path = "hdfs://namenode:9000/electricity/gold/hourly_patterns"
        
        df_gold_monthly.write.mode("overwrite").parquet(monthly_path)
        df_gold_daily.write.mode("overwrite").parquet(daily_path)
        df_gold_hourly.write.mode("overwrite").parquet(hourly_path)
        
        # Create Hive external tables untuk Gold layer
        self.spark.sql(f"""
            CREATE DATABASE IF NOT EXISTS electricity_gold
        """)
        
        # Monthly aggregation table
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS electricity_gold.monthly_consumption (
                region string,
                month string,
                total_kwh double,
                avg_kwh double,
                avg_temp double,
                total_rain double,
                total_outages int,
                total_readings int,
                avg_voltage double,
                avg_current double,
                avg_power_factor double,
                avg_humidity double,
                avg_wind_speed double
            )
            USING PARQUET
            LOCATION '{monthly_path}'
        """)
        
        # Daily aggregation table
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS electricity_gold.daily_consumption (
                region string,
                date date,
                daily_total_kwh double,
                daily_avg_kwh double,
                daily_avg_temp double,
                daily_total_rain double,
                daily_total_outages int,
                daily_total_readings int
            )
            USING PARQUET
            LOCATION '{daily_path}'
        """)
        
        # Hourly patterns table
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS electricity_gold.hourly_patterns (
                region string,
                hour int,
                hourly_avg_kwh double,
                hourly_readings int
            )
            USING PARQUET
            LOCATION '{hourly_path}'
        """)
        
        logger.info("Gold layer created successfully")
        logger.info(f"Monthly aggregations: {df_gold_monthly.count()} records")
        logger.info(f"Daily aggregations: {df_gold_daily.count()} records")
        logger.info(f"Hourly patterns: {df_gold_hourly.count()} records")

    def create_analytics_views(self):
        """
        Create analytical views untuk Superset
        """
        logger.info("Creating analytics views...")
        
        # Regional performance view
        self.spark.sql("""
            CREATE OR REPLACE VIEW electricity_gold.regional_performance AS
            SELECT 
                region,
                SUM(total_kwh) as total_annual_kwh,
                AVG(avg_kwh) as avg_monthly_kwh,
                AVG(avg_temp) as avg_temperature,
                SUM(total_rain) as total_annual_rain,
                SUM(total_outages) as total_annual_outages,
                SUM(total_readings) as total_readings
            FROM electricity_gold.monthly_consumption
            GROUP BY region
            ORDER BY total_annual_kwh DESC
        """)
        
        # Weather impact view
        self.spark.sql("""
            CREATE OR REPLACE VIEW electricity_gold.weather_impact AS
            SELECT 
                month,
                AVG(total_kwh) as avg_monthly_consumption,
                AVG(avg_temp) as avg_temperature,
                AVG(total_rain) as avg_rainfall,
                CORR(total_kwh, avg_temp) as temp_correlation,
                CORR(total_kwh, total_rain) as rain_correlation
            FROM electricity_gold.monthly_consumption
            GROUP BY month
            ORDER BY month
        """)
        
        # Peak hours analysis
        self.spark.sql("""
            CREATE OR REPLACE VIEW electricity_gold.peak_hours AS
            SELECT 
                hour,
                AVG(hourly_avg_kwh) as avg_consumption,
                SUM(hourly_readings) as total_readings
            FROM electricity_gold.hourly_patterns
            GROUP BY hour
            ORDER BY hour
        """)
        
        logger.info("Analytics views created successfully")

    def run_full_pipeline(self):
        """
        Run the complete ETL pipeline
        """
        logger.info("Starting complete ETL pipeline...")
        
        try:
            # Execute pipeline stages
            self.create_bronze_layer()
            self.create_silver_layer()
            self.create_gold_layer()
            self.create_analytics_views()
            
            logger.info("ETL Pipeline completed successfully!")
            
            # Show some statistics
            self.show_pipeline_stats()
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise
        finally:
            self.spark.stop()

    def show_pipeline_stats(self):
        """
        Display pipeline statistics
        """
        print("\n" + "="*50)
        print("PIPELINE STATISTICS")
        print("="*50)
        
        # Bronze stats
        bronze_count = self.spark.table("electricity_bronze.raw_data").count()
        print(f"Bronze Layer: {bronze_count:,} raw records")
        
        # Silver stats
        silver_count = self.spark.table("electricity_silver.cleaned_data").count()
        print(f"Silver Layer: {silver_count:,} cleaned records")
        
        # Gold stats
        monthly_count = self.spark.table("electricity_gold.monthly_consumption").count()
        daily_count = self.spark.table("electricity_gold.daily_consumption").count()
        hourly_count = self.spark.table("electricity_gold.hourly_patterns").count()
        
        print(f"Gold Layer - Monthly: {monthly_count:,} aggregations")
        print(f"Gold Layer - Daily: {daily_count:,} aggregations")
        print(f"Gold Layer - Hourly: {hourly_count:,} patterns")
        
        # Regional breakdown
        print("\nRegional Consumption Summary:")
        self.spark.table("electricity_gold.regional_performance").show(truncate=False)
        
        print("\n" + "="*50)

if __name__ == "__main__":
    etl = ElectricityETL()
    etl.run_full_pipeline()
