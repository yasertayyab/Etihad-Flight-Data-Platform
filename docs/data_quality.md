# Data Quality Strategy

This platform uses Delta Live Tables and Databricks quality expectations to enforce Data Quality eXpressions (DQX) across the pipeline.

## Bronze layer

- Expect source schema fields to be present.
- Preserve raw landing records for audit and replay.

## Silver layer

- Validate required fields: `FlightDate`, `Carrier`, `Origin`, `Dest`, `Distance`.
- Enforce business rules:
  - `Distance > 0`
  - `Cancelled` is 0 or 1
  - `DepDelay` and `ArrDelay` are numeric

## Gold layer

- Aggregate only high-quality records.
- Compute KPIs for flight delay trends and route reliability.
- Store results in Unity Catalog for analytics and BI.

## Operational recovery

- Use bronze raw history to replay missing or failed transactions.
- Reprocess suspicious batches with DLT incremental refresh.
- Monitor quality metrics and set alerts on expectation failures.
