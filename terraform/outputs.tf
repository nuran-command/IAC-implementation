output "public_ip" {
  value       = aws_instance.sre_server.public_ip
  description = "The public IP of the SRE server"
}

output "ssh_command" {
  value       = "ssh -i my-project-key.pem ubuntu@${aws_instance.sre_server.public_ip}"
  description = "Command to SSH into the EC2 instance (Port 22)"
}

output "frontend_url" {
  value       = "http://${aws_instance.sre_server.public_ip}:${var.http_port}"
  description = "Frontend application URL"
}

output "grafana_url" {
  value       = "http://${aws_instance.sre_server.public_ip}:${var.grafana_port}"
  description = "Grafana dashboard URL"
}

output "prometheus_url" {
  value       = "http://${aws_instance.sre_server.public_ip}:${var.prometheus_port}"
  description = "Prometheus UI URL"
}