variable "namespace" {
  type    = string
  default = null
}

variable "deployment_name" {
  type    = string
  default = null
}

variable "container_name" {
  type    = string
  default = null
}

variable "labels" {
  type    = map(string)
  default = null
}

variable "image" {
  type    = string
  default = null
}

variable "replicas" {
  type    = string
  default = "3"
}

variable "max_surge" {
  type    = string
  default = null
}

variable "max_unavailable" {
  type    = string
  default = null
}

variable "command" {
  type    = list(string)
  default = null
}



resource "kubernetes_deployment" "project-x-deployment" {
  metadata {
    name      = var.deployment_name
    namespace = var.namespace
    labels    = var.labels
  }

  spec {
    replicas = var.replicas

    strategy {
      type = "RollingUpdate"

      rolling_update {
        max_surge       = var.max_surge
        max_unavailable = var.max_unavailable
      }
    }

    selector {
      match_labels = var.labels
    }

    template {
      metadata {
        labels = var.labels
      }

      spec {
        container {
          image = var.image
          name  = var.container_name

          readiness_probe {
            exec {
              command = var.command
            }
          }
        }
      }
    }
  }
}
