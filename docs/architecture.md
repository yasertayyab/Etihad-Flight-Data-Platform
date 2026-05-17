# Architecture Overview

This solution is a demonstration of an enterprise Databricks platform for aviation operations analytics. It includes staged data ingestion, Delta Lake storage, Unity Catalog governance, Delta Live Tables orchestration, Lakeflow pipeline control, and CI/CD-driven infrastructure deployment.

## Layers

- **Landing / Raw zone**: CSV flight records streamed by Autoloader into cloud storage.
- **Bronze zone**: Ingested raw flight data persisted as Delta tables in the bronze layer.
- **Silver zone**: Cleansed, normalized flight records with business-level quality checks.
- **Gold zone**: Aggregated KPIs for delay analysis, route performance, and operational dashboards.

## Key components

- `src/ingestion/autoloader_ingest.py`
  - Uses Databricks Autoloader for incremental CSV ingest into Delta.
- `src/dlt/flight_dlt_pipeline.py`
  - Defines bronze, silver, and gold DLT tables and DQ expectations.
- `infra/terraform/`
  - Terraform resources for Databricks cluster, catalog, schema, and DLT job.
- `lakeflow/flight_data_workflow.yaml`
  - Orchestrates ingestion and DLT execution as a Lakeflow workflow.
- `cicd/.github/workflows/databricks-ci.yml`
  - GitHub Actions flow for Terraform validation and deployment.

## Dataset selection

The chosen dataset is the BTS Airline On-Time Performance dataset, which is directly relevant for airline operations analytics and supports use cases like:

- flight delay monitoring
- on-time performance reporting
- route reliability scoring
- cancellation impact analysis

It is a strong match for Etihad’s product-focused data platform goals.
