variable "databricks_host" {
  description = "Databricks workspace URL"
  type        = string
}

variable "databricks_token" {
  description = "Databricks personal access token"
  type        = string
  sensitive   = true
}

variable "catalog_name" {
  description = "Unity Catalog catalog name"
  type        = string
  default     = "etihad_platform"
}

variable "schema_name" {
  description = "Unity Catalog schema for analytics"
  type        = string
  default     = "aviation"
}

variable "storage_root" {
  description = "Cloud storage root for landing, bronze, silver, gold zones"
  type        = string
}

variable "cluster_name" {
  description = "Databricks cluster name"
  type        = string
  default     = "flight-platform-cluster"
}

variable "spark_version" {
  description = "Databricks runtime version"
  type        = string
  default     = "12.2.x-scala2.12"
}

variable "node_type_id" {
  description = "Databricks node type"
  type        = string
  default     = "Standard_DS3_v2"
}
