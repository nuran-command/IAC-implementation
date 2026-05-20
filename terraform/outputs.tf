output "public_ip" {
  value = aws_eip.sre_eip.public_ip
}

output "ssh_commands" {
  value       = [for ip in aws_instance.sre_server[*].public_ip : "ssh -i ${var.key_name}.pem ubuntu@${ip}"]
  description = "Commands to SSH into the EC2 instances"
}

output "manager_node_ip" {
  value       = aws_instance.sre_server[0].public_ip
  description = "The public IP of the primary Manager node"
}

output "frontend_url" {
  value       = "http://${aws_instance.sre_server[0].public_ip}:${var.http_port}"
  description = "Frontend application URL (Standard)"
}

output "frontend_url_k8s" {
  value       = "http://${aws_instance.sre_server[0].public_ip}:30080"
  description = "Frontend application URL (Kubernetes NodePort)"
}

output "grafana_url" {
  value       = "http://${aws_instance.sre_server[0].public_ip}:30300"
  description = "Grafana dashboard URL (Kubernetes NodePort)"
}

output "prometheus_url" {
  value       = "http://${aws_instance.sre_server[0].public_ip}:30090"
  description = "Prometheus UI URL (Kubernetes NodePort)"
}