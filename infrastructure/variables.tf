# Variable definitions

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "service_name" {
  description = "The name of the Cloud Run service"
  type        = string
  default     = "flask-hello-world-api"
}

variable "service_account_name" {
  description = "The name of the service account for Cloud Run"
  type        = string
  default     = "flask-hello-world-sa"
}

variable "artifact_registry_repository_id" {
  description = "The ID of the Artifact Registry repository"
  type        = string
  default     = "flask-hello-world-repo"
}

variable "container_image" {
  description = "The container image to deploy. Leave empty to use default from Artifact Registry"
  type        = string
  default     = ""
}

variable "container_port" {
  description = "The port the container listens on"
  type        = number
  default     = 8080
}

variable "flask_env" {
  description = "Flask environment (production, development)"
  type        = string
  default     = "production"
}

variable "secret_key" {
  description = "Secret key for Flask (use Secret Manager in production)"
  type        = string
  default     = ""
  sensitive   = true
}

variable "cpu_limit" {
  description = "CPU limit for the container"
  type        = string
  default     = "1000m"
  
  validation {
    condition     = can(regex("^[0-9]+m?$", var.cpu_limit))
    error_message = "CPU limit must be a valid CPU value (e.g., 1000m, 2)."
  }
}

variable "memory_limit" {
  description = "Memory limit for the container"
  type        = string
  default     = "512Mi"
  
  validation {
    condition     = can(regex("^[0-9]+(Mi|Gi)$", var.memory_limit))
    error_message = "Memory limit must be a valid memory value (e.g., 512Mi, 2Gi)."
  }
}

variable "cpu_always_allocated" {
  description = "Whether CPU should always be allocated (true) or only during request processing (false)"
  type        = bool
  default     = false
}

variable "min_instance_count" {
  description = "Minimum number of instances"
  type        = number
  default     = 0
  
  validation {
    condition     = var.min_instance_count >= 0
    error_message = "Minimum instance count must be >= 0."
  }
}

variable "max_instance_count" {
  description = "Maximum number of instances"
  type        = number
  default     = 10
  
  validation {
    condition     = var.max_instance_count >= 1 && var.max_instance_count <= 1000
    error_message = "Maximum instance count must be between 1 and 1000."
  }
}

variable "max_instance_request_concurrency" {
  description = "Maximum number of concurrent requests per instance"
  type        = number
  default     = 80
  
  validation {
    condition     = var.max_instance_request_concurrency >= 1 && var.max_instance_request_concurrency <= 1000
    error_message = "Max instance request concurrency must be between 1 and 1000."
  }
}

variable "allow_unauthenticated" {
  description = "Whether to allow unauthenticated access to the service"
  type        = bool
  default     = true
}

variable "deletion_protection" {
  description = "Whether to enable deletion protection on the Cloud Run service"
  type        = bool
  default     = false
}

variable "enable_monitoring" {
  description = "Whether to enable monitoring and alerting"
  type        = bool
  default     = false
}

variable "notification_channels" {
  description = "List of notification channel IDs for alerts"
  type        = list(string)
  default     = []
}

variable "labels" {
  description = "Labels to apply to resources"
  type        = map(string)
  default = {
    app         = "flask-hello-world"
    environment = "production"
    managed_by  = "terraform"
  }
}