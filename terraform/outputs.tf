output "public_ip" {
  value       = aws_instance.sre_server.public_ip
  description = "The public IP of the SRE server"
}

output "ssh_command" {
  value       = "ssh -i my-project-key.pem ubuntu@${aws_instance.sre_server.public_ip}"
  description = "Command to SSH into the EC2 instance (Port 22)"
}

output "frontend_url" {
  value       = "http://${aws_instance.sre_server.public_ip}:80"
  description = "Frontend application URL (Port 80)"
}

output "grafana_url" {
  value       = "http://${aws_instance.sre_server.public_ip}:3000"
  description = "Grafana dashboard URL (Port 3000)"
}

output "prometheus_url" {
  value       = "http://${aws_instance.sre_server.public_ip}:9090"
  description = "Prometheus UI URL (Port 9090)"
}