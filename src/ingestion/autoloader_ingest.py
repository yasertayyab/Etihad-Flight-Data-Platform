from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DateType


def create_spark_session():
    return SparkSession.builder.appName("flight-autoloader-ingest").getOrCreate()


def flight_schema():
    return StructType([
        StructField("FlightDate", DateType(), True),
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


def run_autoloader(landing_path: str, bronze_path: str, checkpoint_path: str):
    spark = create_spark_session()
    df = (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("inferSchema", "false")
        .schema(flight_schema())
        .load(landing_path)
    )

    query = (
        df.writeStream
        .format("delta")
        .option("checkpointLocation", checkpoint_path)
        .outputMode("append")
        .option("mergeSchema", "true")
        .start(bronze_path)
    )

    query.awaitTermination()


if __name__ == "__main__":
    import os

    landing_path = os.getenv("LANDING_PATH", "/mnt/landing/flight_data")
    bronze_path = os.getenv("BRONZE_PATH", "/mnt/bronze/flight_data")
    checkpoint_path = os.getenv("CHECKPOINT_PATH", "/mnt/checkpoints/autoloader_flight")

    run_autoloader(landing_path, bronze_path, checkpoint_path)
