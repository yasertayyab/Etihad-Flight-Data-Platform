from pyspark.sql import DataFrame


def enforce_quality(df: DataFrame) -> DataFrame:
    """Add business validation checks for flight operational records."""
    return (
        df.filter("FlightDate IS NOT NULL")
          .filter("Origin IS NOT NULL")
          .filter("Dest IS NOT NULL")
          .filter("Distance > 0")
          .filter("Cancelled IN (0,1)")
    )
