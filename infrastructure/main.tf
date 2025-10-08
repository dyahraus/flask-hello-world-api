# Main Terraform configuration

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  # Uncomment and configure for remote state storage
  # backend "gcs" {
  #   bucket = "your-terraform-state-bucket"
  #   prefix = "terraform/state/flask-hello-world-api"
  # }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "run_api" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifact_registry_api" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild_api" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

# Artifact Registry Repository for container images
resource "google_artifact_registry_repository" "flask_app_repo" {
  location      = var.region
  repository_id = var.artifact_registry_repository_id
  description   = "Container repository for Flask Hello World API"
  format        = "DOCKER"

  depends_on = [google_project_service.artifact_registry_api]
}

# Service Account for Cloud Run
resource "google_service_account" "flask_app_sa" {
  account_id   = var.service_account_name
  display_name = "Flask Hello World API Service Account"
  description  = "Service account for Flask Hello World API running on Cloud Run"
}

# IAM binding for service account (if needed to access other GCP services)
# Uncomment and modify as needed
# resource "google_project_iam_member" "flask_app_sa_logging" {
#   project = var.project_id
#   role    = "roles/logging.logWriter"
#   member  = "serviceAccount:${google_service_account.flask_app_sa.email}"
# }

# Cloud Run Service
resource "google_cloud_run_v2_service" "flask_app" {
  name     = var.service_name
  location = var.region
  
  deletion_protection = var.deletion_protection

  template {
    service_account = google_service_account.flask_app_sa.email
    
    scaling {
      min_instance_count = var.min_instance_count
      max_instance_count = var.max_instance_count
    }

    containers {
      # This is a placeholder - you'll need to build and push your image first
      image = var.container_image != "" ? var.container_image : "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.flask_app_repo.repository_id}/flask-hello-world:latest"

      ports {
        container_port = var.container_port
      }

      resources {
        limits = {
          cpu    = var.cpu_limit
          memory = var.memory_limit
        }
        
        cpu_idle = var.cpu_always_allocated
        startup_cpu_boost = true
      }

      env {
        name  = "FLASK_ENV"
        value = var.flask_env
      }

      env {
        name  = "PORT"
        value = tostring(var.container_port)
      }

      # Secret key for Flask - use Secret Manager in production
      dynamic "env" {
        for_each = var.secret_key != "" ? [1] : []
        content {
          name  = "SECRET_KEY"
          value = var.secret_key
        }
      }

      # Liveness probe
      liveness_probe {
        http_get {
          path = "/health"
          port = var.container_port
        }
        initial_delay_seconds = 10
        timeout_seconds       = 3
        period_seconds        = 30
        failure_threshold     = 3
      }

      # Startup probe
      startup_probe {
        http_get {
          path = "/health"
          port = var.container_port
        }
        initial_delay_seconds = 0
        timeout_seconds       = 3
        period_seconds        = 10
        failure_threshold     = 3
      }
    }

    timeout = "300s"
    
    max_instance_request_concurrency = var.max_instance_request_concurrency
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_service.run_api,
    google_artifact_registry_repository.flask_app_repo
  ]

  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
    ]
  }
}

# IAM policy to allow public access (if needed)
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  count = var.allow_unauthenticated ? 1 : 0

  location = google_cloud_run_v2_service.flask_app.location
  name     = google_cloud_run_v2_service.flask_app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# IAM policy for authenticated access only
resource "google_cloud_run_v2_service_iam_member" "authenticated_access" {
  count = var.allow_unauthenticated ? 0 : 1

  location = google_cloud_run_v2_service.flask_app.location
  name     = google_cloud_run_v2_service.flask_app.name
  role     = "roles/run.invoker"
  member   = "allAuthenticatedUsers"
}

# Cloud Monitoring Alert Policy for service availability (optional)
resource "google_monitoring_alert_policy" "flask_app_availability" {
  count = var.enable_monitoring ? 1 : 0

  display_name = "${var.service_name}-availability-alert"
  combiner     = "OR"
  
  conditions {
    display_name = "Service availability check"
    
    condition_threshold {
      filter          = "resource.type = \"cloud_run_revision\" AND resource.labels.service_name = \"${var.service_name}\" AND metric.type = \"run.googleapis.com/request_count\""
      duration        = "300s"
      comparison      = "COMPARISON_LT"
      threshold_value = 1
      
      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = var.notification_channels

  alert_strategy {
    auto_close = "1800s"
  }
}