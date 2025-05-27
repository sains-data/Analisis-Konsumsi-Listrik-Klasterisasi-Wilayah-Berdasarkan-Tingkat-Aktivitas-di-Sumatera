# Electricity Data Analysis - Enhanced Notebook
# Bronze -> Silver -> Gold Pipeline dengan PySpark dan Hive

import pandas as pd
import numpy as np
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("ElectricityAnalysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .enableHiveSupport() \
    .getOrCreate()

print("✅ Spark Session initialized successfully!")

# =============================================================================
# BRONZE LAYER - Data Ingestion
# =============================================================================

print("📥 Loading data from Bronze layer...")

# Read data dari local file (jika HDFS belum ready)
try:
    df_bronze_spark = spark.table("electricity_bronze.raw_data")
    print("✅ Data loaded from Hive table")
except:
    # Fallback ke local file
    df_bronze = pd.read_csv("/home/jovyan/work/bronze/data_listrik_raw.csv")
    df_bronze_spark = spark.createDataFrame(df_bronze)
    print("✅ Data loaded from local CSV")

print(f"📊 Bronze layer: {df_bronze_spark.count():,} records")
df_bronze_spark.printSchema()

# =============================================================================
# SILVER LAYER - Data Cleaning & Transformation
# =============================================================================

print("\n🧹 Processing Silver layer...")

# Data cleaning operations
df_silver = df_bronze_spark \
    .filter(col("power_consumption").isNotNull()) \
    .filter(col("region").isNotNull()) \
    .filter(col("timestamp").isNotNull()) \
    .withColumn("timestamp", to_timestamp(col("timestamp"))) \
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
    .withColumn("day_of_week", dayofweek(col("timestamp"))) \
    .filter(col("power_consumption") > 0)

print(f"📊 Silver layer: {df_silver.count():,} records after cleaning")

# Cache untuk performa
df_silver.cache()

# =============================================================================
# GOLD LAYER - Aggregations & Analytics
# =============================================================================

print("\n📈 Creating Gold layer aggregations...")

# 1. Monthly aggregations by region
df_gold_monthly = df_silver.groupBy("region", "month") \
    .agg(
        sum("power_consumption").alias("total_kwh"),
        avg("power_consumption").alias("avg_kwh"),
        avg("temperature").alias("avg_temp"),
        sum("rainfall").alias("total_rain"),
        sum(when(col("outage_flag") == True, 1).otherwise(0)).alias("total_outages"),
        count("*").alias("total_readings"),
        avg("voltage").alias("avg_voltage"),
        avg("current").alias("avg_current"),
        avg("power_factor").alias("avg_power_factor"),
        stddev("power_consumption").alias("std_consumption")
    )

# 2. Daily patterns
df_gold_daily = df_silver.groupBy("region", "date", "day_of_week") \
    .agg(
        sum("power_consumption").alias("daily_total_kwh"),
        avg("power_consumption").alias("daily_avg_kwh"),
        max("power_consumption").alias("daily_peak_kwh"),
        min("power_consumption").alias("daily_min_kwh"),
        avg("temperature").alias("daily_avg_temp")
    )

# 3. Hourly patterns untuk load profiling
df_gold_hourly = df_silver.groupBy("region", "hour") \
    .agg(
        avg("power_consumption").alias("hourly_avg_kwh"),
        max("power_consumption").alias("hourly_peak_kwh"),
        count("*").alias("hourly_readings"),
        stddev("power_consumption").alias("hourly_std_kwh")
    )

# 4. Weather correlation analysis
df_weather_corr = df_silver.groupBy("region") \
    .agg(
        corr("power_consumption", "temperature").alias("temp_correlation"),
        corr("power_consumption", "humidity").alias("humidity_correlation"),
        corr("power_consumption", "rainfall").alias("rainfall_correlation"),
        corr("power_consumption", "wind_speed").alias("wind_correlation")
    )

print("✅ Gold layer aggregations completed")

# =============================================================================
# DATA VISUALIZATION & ANALYSIS
# =============================================================================

print("\n📊 Creating visualizations...")

# Convert to Pandas untuk plotting
monthly_pd = df_gold_monthly.toPandas()
hourly_pd = df_gold_hourly.toPandas()
daily_pd = df_gold_daily.toPandas()
weather_pd = df_weather_corr.toPandas()

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# 1. Regional Consumption Comparison
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Total consumption by region
region_total = monthly_pd.groupby('region')['total_kwh'].sum().sort_values(ascending=False)
axes[0,0].bar(range(len(region_total)), region_total.values)
axes[0,0].set_xticks(range(len(region_total)))
axes[0,0].set_xticklabels(region_total.index, rotation=45, ha='right')
axes[0,0].set_title('Total Electricity Consumption by Region')
axes[0,0].set_ylabel('Total kWh')

# Average temperature by region
region_temp = monthly_pd.groupby('region')['avg_temp'].mean().sort_values(ascending=False)
axes[0,1].bar(range(len(region_temp)), region_temp.values, color='orange')
axes[0,1].set_xticks(range(len(region_temp)))
axes[0,1].set_xticklabels(region_temp.index, rotation=45, ha='right')
axes[0,1].set_title('Average Temperature by Region')
axes[0,1].set_ylabel('Temperature (°C)')

# Hourly load profile
hourly_avg = hourly_pd.groupby('hour')['hourly_avg_kwh'].mean()
axes[1,0].plot(hourly_avg.index, hourly_avg.values, marker='o', linewidth=2)
axes[1,0].set_title('Average Hourly Load Profile')
axes[1,0].set_xlabel('Hour of Day')
axes[1,0].set_ylabel('Average kWh')
axes[1,0].grid(True, alpha=0.3)

# Outages by region
region_outages = monthly_pd.groupby('region')['total_outages'].sum().sort_values(ascending=False)
axes[1,1].bar(range(len(region_outages)), region_outages.values, color='red', alpha=0.7)
axes[1,1].set_xticks(range(len(region_outages)))
axes[1,1].set_xticklabels(region_outages.index, rotation=45, ha='right')
axes[1,1].set_title('Total Outages by Region')
axes[1,1].set_ylabel('Number of Outages')

plt.tight_layout()
plt.show()

# 2. Interactive Plotly Charts
print("Creating interactive charts...")

# Monthly consumption trends
fig_monthly = px.line(monthly_pd, x='month', y='total_kwh', color='region',
                     title='Monthly Electricity Consumption Trends by Region',
                     labels={'total_kwh': 'Total Consumption (kWh)', 'month': 'Month'})
fig_monthly.show()

# Temperature vs Consumption correlation
fig_scatter = px.scatter(monthly_pd, x='avg_temp', y='avg_kwh', color='region',
                        size='total_readings', hover_data=['month'],
                        title='Temperature vs Average Consumption by Region',
                        labels={'avg_temp': 'Average Temperature (°C)', 
                               'avg_kwh': 'Average Consumption (kWh)'})
fig_scatter.show()

# Heatmap of hourly consumption patterns
hourly_pivot = hourly_pd.pivot(index='region', columns='hour', values='hourly_avg_kwh')
fig_heatmap = px.imshow(hourly_pivot, 
                       title='Hourly Consumption Patterns by Region',
                       labels=dict(x="Hour of Day", y="Region", color="Avg kWh"))
fig_heatmap.show()

# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

print("\n📈 Statistical Analysis Results:")
print("="*50)

# Regional statistics
print("Top 5 Regions by Total Consumption:")
top_regions = monthly_pd.groupby('region')['total_kwh'].sum().sort_values(ascending=False).head()
for region, consumption in top_regions.items():
    print(f"  {region}: {consumption:,.0f} kWh")

print(f"\nOverall Statistics:")
total_consumption = monthly_pd['total_kwh'].sum()
avg_consumption = monthly_pd['avg_kwh'].mean()
print(f"  Total Consumption: {total_consumption:,.0f} kWh")
print(f"  Average Consumption: {avg_consumption:.2f} kWh")

# Peak hours analysis
peak_hours = hourly_pd.groupby('hour')['hourly_avg_kwh'].mean().sort_values(ascending=False).head(3)
print(f"\nPeak Consumption Hours:")
for hour, consumption in peak_hours.items():
    print(f"  Hour {hour}:00 - {consumption:.2f} kWh")

# Weather correlation insights
print(f"\nWeather Correlation Analysis:")
print(weather_pd.to_string(index=False))

# =============================================================================
# EXPORT TO DIFFERENT FORMATS
# =============================================================================

print("\n💾 Exporting processed data...")

# Export to local files for Superset
monthly_pd.to_csv('/home/jovyan/work/gold/monthly_consumption.csv', index=False)
hourly_pd.to_csv('/home/jovyan/work/gold/hourly_patterns.csv', index=False)
daily_pd.to_csv('/home/jovyan/work/gold/daily_consumption.csv', index=False)
weather_pd.to_csv('/home/jovyan/work/gold/weather_correlation.csv', index=False)

# Export to Parquet (if HDFS is available)
try:
    df_gold_monthly.write.mode("overwrite").parquet("hdfs://namenode:9000/electricity/gold/monthly")
    df_gold_hourly.write.mode("overwrite").parquet("hdfs://namenode:9000/electricity/gold/hourly")
    df_gold_daily.write.mode("overwrite").parquet("hdfs://namenode:9000/electricity/gold/daily")
    print("✅ Data exported to HDFS successfully")
except:
    print("⚠️ HDFS not available, data saved locally only")

print("\n🎉 Analysis completed successfully!")
print("📁 Output files saved in /gold/ directory")
print("🔗 Ready for Superset dashboard creation!")
