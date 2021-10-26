variable "config_path" {
  type    = string
  default = null
}

variable "config_context" {
  type    = string
  default = null
}

variable "insecure" {
  type    = string
  default = null
}

provider "kubernetes" {
  config_path    = var.config_path
  config_context = var.config_context
  insecure       = var.insecure
}
