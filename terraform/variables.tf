variable "region" {
  default = "us-east-1"
  description = "AWS region to deploy in"
}

variable "environment" {
  default     = "production"
  description = "Deployment environment (e.g. production, staging)"
}

variable "instance_type" {
  default     = "t3.medium"
  description = "EC2 instance type for vertical scaling"
}

variable "node_count" {
  default     = 1
  description = "Number of worker nodes to provision (Horizontal Scaling)"
}

variable "key_name" {
  default     = "my-project-key"
  description = "Name of the AWS SSH key pair"
}

variable "ssh_port" {
  default     = 22
  description = "SSH port"
  type        = number
}

variable "http_port" {
  default     = 80
  description = "Standard HTTP port for Frontend"
  type        = number
}

variable "grafana_port" {
  default     = 3000
  description = "Grafana dashboard port"
  type        = number
}

variable "prometheus_port" {
  default     = 9090
  description = "Prometheus UI port"
  type        = number
}

variable "redis_port" {
  default     = 6379
  description = "Redis standard port"
  type        = number
}

variable "swarm_port" {

  default     = 2377
  description = "Docker Swarm cluster management port"
  type        = number
}

variable "k8s_nodeport_min" {
  default     = 30000
  description = "Minimum port in Kubernetes NodePort range"
  type        = number
}

variable "k8s_nodeport_max" {
  default     = 32767
  description = "Maximum port in Kubernetes NodePort range"
  type        = number
}