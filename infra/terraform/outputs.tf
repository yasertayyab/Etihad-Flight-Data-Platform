output "databricks_catalog_name" {
  description = "Unity Catalog catalog name"
  value       = databricks_catalog.platform_catalog.name
}

output "databricks_schema_name" {
  description = "Unity Catalog schema name"
  value       = databricks_schema.analytics_schema.name
}

output "databricks_cluster_id" {
  description = "Databricks cluster ID for the analytics platform"
  value       = databricks_cluster.platform_cluster.id
}

output "flight_dlt_job_id" {
  description = "Databricks job ID for the flight DLT pipeline"
  value       = databricks_job.flight_dlt_pipeline.id
}
