terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  # Hide port logic inside locals for a cleaner main.tf
  ingress_rules = [
    { port = var.ssh_port, desc = "SSH" },
    { port = var.http_port, desc = "Standard HTTP" },
    { port = var.grafana_port, desc = "Grafana" },
    { port = var.prometheus_port, desc = "Prometheus" },
    { port = var.redis_port, desc = "Redis (Internal/Debug)" }
  ]
}


# 1. Create a Security Group
resource "aws_security_group" "sre_sg" {
  name        = "sre-project-sg-${var.environment}"
  description = "Allow inbound traffic for SRE project microservices"

  # Dynamic ingress for standard ports
  dynamic "ingress" {
    for_each = local.ingress_rules
    content {
      description = ingress.value.desc
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  # Kubernetes NodePort Range (Abstracted from main logic)
  ingress {
    description = "Kubernetes NodePorts"
    from_port   = var.k8s_nodeport_min
    to_port     = var.k8s_nodeport_max
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Docker Swarm Cluster Communication (Internal/Self)
  ingress {
    description = "Swarm Internal"
    from_port   = var.swarm_port
    to_port     = var.swarm_port
    protocol    = "tcp"
    self        = true
  }

  # Allow all outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "sre-security-group"
    Environment = var.environment
    Project     = "EndTerm-SRE"
  }
}


# 2. Create EC2 Instances
resource "aws_instance" "sre_server" {
  count         = var.node_count
  ami           = "ami-0c7217cdde317cfec" # Ubuntu 22.04 LTS in us-east-1
  instance_type = var.instance_type
  key_name      = var.key_name

  vpc_security_group_ids = [aws_security_group.sre_sg.id]

  tags = {
    Name        = "SRE-Node-${count.index + 1}"
    Environment = var.environment
    Project     = "EndTerm-SRE"
    Role        = count.index == 0 ? "Manager" : "Worker"
  }
}

