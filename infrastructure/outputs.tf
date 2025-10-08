# Output definitions

output "service_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.flask_app.uri
}

output "service_name" {
  description = "The name of the Cloud Run service"
  value       = google_cloud_run_v2_service.flask_app.name
}

output "service_id" {
  description = "The ID of the Cloud Run service"
  value       = google_cloud_run_v2_service.flask_app.id
}

output "service_location" {
  description = "The location of the Cloud Run service"
  value       = google_cloud_run_v2_service.flask_app.location
}

output "service_account_email" {
  description = "The email of the service account used by Cloud Run"
  value       = google_service_account.flask_app_sa.email
}

output "artifact_registry_repository" {
  description = "The name of the Artifact Registry repository"
  value       = google_artifact_registry_repository.flask_app_repo.name
}

output "artifact_registry_repository_url" {
  description = "The URL for pushing images to Artifact Registry"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.flask_app_repo.repository_id}"
}

output "latest_revision" {
  description = "The latest ready revision of the service"
  value       = google_cloud_run_v2_service.flask_app.latest_ready_revision
}

output "health_check_endpoint" {
  description = "The health check endpoint URL"
  value       = "${google_cloud_run_v2_service.flask_app.uri}/health"
}