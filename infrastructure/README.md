# Flask Hello World API - GCP Infrastructure

This repository contains Terraform configuration for deploying the Flask Hello World API to Google Cloud Platform using Cloud Run.

## Architecture

The infrastructure includes:

- **Cloud Run Service**: Serverless container deployment for the Flask API
- **Artifact Registry**: Container image repository
- **Service Account**: Dedicated identity for the Cloud Run service
- **IAM Policies**: Access control for the service
- **Monitoring** (optional): Alert policies for service availability

## Prerequisites

1. **Google Cloud Platform Account** with billing enabled
2. **GCP Project** created
3. **Terraform** (>= 1.0) installed
4. **gcloud CLI** installed and authenticated
5. **Docker** installed (for building container images)
6. Appropriate IAM permissions:
   - Cloud Run Admin
   - Service Account Admin
   - Artifact Registry Admin
   - Project IAM Admin

## Initial Setup

### 1. Authenticate with GCP