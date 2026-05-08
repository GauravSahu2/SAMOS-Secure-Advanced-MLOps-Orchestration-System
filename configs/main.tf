# Phase 6: Infrastructure as Code (Terraform)
# This defines the "Environment" for the pipeline

provider "local" {}

resource "local_file" "infra_status" {
  filename = "${path.module}/infra_manifest.txt"
  content  = <<EOT
  MLOps Infrastructure Manifest
  ----------------------------
  Compute: Local Python 3.10
  Storage: Local SSD (data/ directory)
  Tracking: MLflow (sqlite)
  Registry: MLflow Model Registry
  EOT
}

# Placeholder for Cloud (AWS/GCP/Azure)
# resource "aws_s3_bucket" "data_lake" {
#   bucket = "ml-pipeline-bronze-data"
# }
