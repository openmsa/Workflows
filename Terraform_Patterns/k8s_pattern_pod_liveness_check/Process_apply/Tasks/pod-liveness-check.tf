variable "namespace" {
  type    = string
  default = null
}

variable "pod_name" {
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

variable "container_port" {
  type    = number
  default = null
}

variable "protocol" {
  type    = string
  default = null
}

variable "http_get_path" {
  type    = string
  default = null
}

variable "http_get_port" {
  type    = string
  default = null
}

variable "initial_delay_seconds" {
  type    = number
  default = null
}


resource "kubernetes_pod" "project-x-pod" {
  metadata {
    name      = var.pod_name
    namespace = var.namespace
    labels    = var.labels
  }

  spec {
    container {
      image = var.image
      name  = var.container_name
      port {
        container_port = var.container_port
        protocol       = var.protocol
      }
      liveness_probe {
        http_get {
          path = var.http_get_path
          port = var.http_get_port
        }
        initial_delay_seconds = var.initial_delay_seconds
      }
    }
  }
}
