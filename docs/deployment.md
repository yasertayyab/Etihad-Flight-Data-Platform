# Deployment Guide

## Prerequisites

- Databricks workspace and personal access token
- Terraform installed locally
- GitHub repository for CI/CD
- Cloud storage account for landing/bronze/silver/gold zones

## Setup

1. Copy the example vars file:
   ```bash
   cp infra/terraform/terraform.tfvars.example infra/terraform/terraform.tfvars
   ```
2. Update `infra/terraform/terraform.tfvars` with your Databricks host, token, storage path, and cluster details.
3. Install Python dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Deploy infrastructure

1. Initialize Terraform:
   ```bash
   terraform init infra/terraform
   ```
2. Validate configuration:
   ```bash
   terraform validate infra/terraform
   ```
3. Apply infrastructure:
   ```bash
   terraform apply -auto-approve -var-file=infra/terraform/terraform.tfvars
   ```

## Import repo into Databricks

1. In Databricks Repos, connect to this Git repository.
2. Ensure the Python files are available under `/Repos/<your-repo>/src/`.
3. Set the DLT pipeline configuration to use `src/dlt/flight_dlt_pipeline.py`.

## Configure secrets and environment variables

- Store `DATABRICKS_HOST` and `DATABRICKS_TOKEN` in your GitHub repository secrets.
- Use the same values in `infra/terraform/terraform.tfvars`.

## Run the pipeline

- Start the Autoloader ingest job to land CSV files to `landing/flight_data`.
- Execute the DLT pipeline and verify bronze, silver, and gold tables.
- Confirm Lakeflow task orchestration if using the workflow YAML.
