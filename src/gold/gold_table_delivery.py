from pyspark.sql import SparkSession


def create_spark_session():
    return SparkSession.builder.appName("flight-gold-delivery").getOrCreate()


if __name__ == "__main__":
    spark = create_spark_session()
    gold_df = spark.read.format("delta").load("/mnt/gold/flight_performance")
    gold_df.createOrReplaceTempView("gold_flight_performance")
    spark.sql(
        """
        CREATE TABLE IF NOT EXISTS etihad_platform.aviation.gold_flight_performance
        USING DELTA
        LOCATION '/mnt/gold/flight_performance'
        AS SELECT * FROM gold_flight_performance
        """
    )
