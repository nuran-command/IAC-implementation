output "public_ip" {
  value       = aws_instance.sre_server.public_ip
  description = "The public IP of the SRE server"
}