from pyspark.sql.types import StructField, StructType, StringType, IntegerType, DateType


def flight_schema() -> StructType:
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
