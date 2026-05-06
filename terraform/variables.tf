variable "region" {
  default = "us-east-1"
}

variable "instance_type" {
  default = "t3.medium"
}

variable "ssh_port" {
  description = "SSH port"
  type        = number
}

variable "http_port" {
  description = "HTTP port"
  type        = number
}

variable "grafana_port" {
  description = "Grafana port"
  type        = number
}

variable "prometheus_port" {
  description = "Prometheus port"
  type        = number
}