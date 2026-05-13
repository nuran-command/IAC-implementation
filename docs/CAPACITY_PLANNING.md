# Capacity Planning & Automation

## Observations
1. **Resource Consumption:** The `order-service` and `payment-service` consume the most CPU and RAM during peak load simulations.
2. **Bottleneck:** The PostgreSQL database experiences connection saturation during concurrent order creations and payment processings.

## Strategies Implemented
### Horizontal Scaling (Replicas)
- Implemented Docker Swarm service replication and Kubernetes `Deployment` replicas.
- `order-service` is scaled to 3 replicas.
- `payment-service`, `auth-service`, `product-service`, `notification-service`, and `user-profile-service` are scaled to 2 replicas each.
- Nginx reverse proxy load balances incoming requests across the `order-service` instances.

### Vertical Scaling (CPU/RAM)
- Terraform configurations (`terraform/main.tf`) allow adjusting the underlying AWS EC2 instance type (e.g., from `t2.micro` to `t3.medium`) based on the `instance_type` variable, allowing easy vertical scaling.

### Database Optimization
- Connection pooling needs to be configured using PgBouncer.
- Added database resource limits and specific environments to handle load.

## Automation Setup
1. **Automated Deployment:**
   - Handled by Ansible playbooks (`ansible/playbook.yml`) which provisions Docker/Swarm and deploys the stack declaratively.
2. **Health Checks & Restart Policies:**
   - Docker Compose includes `healthcheck` definitions for every API with `curl -f http://localhost/health`.
   - `restart: unless-stopped` guarantees self-healing when the daemon reboots or a container crashes.
3. **Monitoring Alerts:**
   - Prometheus `alert_rules.yml` contains threshold definitions that fire if a service's health endpoint fails.
