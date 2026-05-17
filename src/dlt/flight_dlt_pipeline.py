import dlt
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DateType
from pyspark.sql.functions import col, to_date, when, avg, count, sum as spark_sum


def flight_schema():
    return StructType([
        StructField("FlightDate", StringType(), True),
        StructField("Carrier", StringType(), True),
        StructField("FlightNum", StringType(), True),
        StructField("Origin", StringType(), True),
        StructField("Dest", StringType(), True),
        StructField("DepTime", StringType(), True),
        StructField("ArrTime", StringType(), True),
        StructField("DepDelay", IntegerType(), True),
        StructField("ArrDelay", IntegerType(), True),
        StructField("Cancelled", IntegerType(), True),
        StructField("Diverted", IntegerType(), True),
        StructField("Distance", IntegerType(), True),
    ])


@dlt.table(name="bronze_flights", comment="Bronze layer of raw flight ingestion.")
def bronze_flights():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("mergeSchema", "true")
        .schema(flight_schema())
        .load("/mnt/landing/flight_data")
    )


@dlt.table(name="silver_flights", comment="Silver layer with cleansed flight records.")
@dlt.expect("valid_flight_date", "FlightDate IS NOT NULL")
@dlt.expect("valid_origin", "Origin IS NOT NULL")
@dlt.expect("valid_dest", "Dest IS NOT NULL")
@dlt.expect("positive_distance", "Distance > 0")
@dlt.expect("valid_cancelled_flag", "Cancelled IN (0, 1)")
def silver_flights():
    df = dlt.read("bronze_flights")

    return (
        df.withColumn("FlightDate", to_date(col("FlightDate"), "yyyy-MM-dd"))
          .withColumn("DepTime", when(col("DepTime") == "", None).otherwise(col("DepTime")))
          .withColumn("ArrTime", when(col("ArrTime") == "", None).otherwise(col("ArrTime")))
          .withColumn("Carrier", col("Carrier").alias("Carrier"))
          .withColumn("Origin", col("Origin"))
          .withColumn("Dest", col("Dest"))
          .select(
              "FlightDate",
              "Carrier",
              "FlightNum",
              "Origin",
              "Dest",
              "DepTime",
              "ArrTime",
              "DepDelay",
              "ArrDelay",
              "Cancelled",
              "Diverted",
              "Distance"
          )
    )


@dlt.table(name="gold_flight_performance", comment="Gold layer summarizing flight performance KPIs.")
@dlt.expect("valid_aggregate_keys", "Carrier IS NOT NULL AND Origin IS NOT NULL AND Dest IS NOT NULL")
def gold_flight_performance():
    return (
        dlt.read("silver_flights")
          .groupBy("Carrier", "Origin", "Dest")
          .agg(
              avg("ArrDelay").alias("avg_arrival_delay"),
              avg("DepDelay").alias("avg_departure_delay"),
              spark_sum("Cancelled").alias("cancelled_count"),
              spark_sum("Diverted").alias("diverted_count"),
              count("FlightNum").alias("flight_count")
          )
          .where("flight_count > 0")
    )
