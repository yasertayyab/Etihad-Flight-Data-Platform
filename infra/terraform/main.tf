terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
}

provider "databricks" {
  host  = var.databricks_host
  token = var.databricks_token
}

resource "databricks_catalog" "platform_catalog" {
  name    = var.catalog_name
  comment = "Enterprise Unity Catalog for Etihad flight analytics"
}

resource "databricks_schema" "analytics_schema" {
  name      = var.schema_name
  catalog_name = databricks_catalog.platform_catalog.name
  comment   = "Schema for aviation bronze/silver/gold tables"
}

resource "databricks_cluster" "platform_cluster" {
  cluster_name            = var.cluster_name
  spark_version           = var.spark_version
  node_type_id            = var.node_type_id
  autotermination_minutes = 60
  spark_conf = {
    "spark.databricks.delta.properties.defaults.autoOptimize.optimizeWrite" = "true"
    "spark.databricks.delta.properties.defaults.autoOptimize.autoCompact"  = "true"
  }
}

resource "databricks_job" "flight_dlt_pipeline" {
  name = "flight-dlt-pipeline"

  existing_cluster_id = databricks_cluster.platform_cluster.id

  spark_python_task {
    python_file = "file:/Workspace/Repos/<your-repo>/src/dlt/flight_dlt_pipeline.py"
  }

  max_retries = 1
  timeout_seconds = 7200
}
