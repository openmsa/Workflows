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

variable "command" {
  type    = list(string)
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
      readiness_probe {
        exec {
          command = var.command
        }
      }
    }
  }
}
