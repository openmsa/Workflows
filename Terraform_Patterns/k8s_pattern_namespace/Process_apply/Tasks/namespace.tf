variable "namespace_name" {
  type    = string
  default = null
}

variable "labels" {
  type    = map(string)
  default = null
}


resource "kubernetes_namespace" "project-x-namespace" {
  metadata {
    name   = var.namespace_name
    labels = var.labels
  }
}
