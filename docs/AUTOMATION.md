# Automation & Capacity Planning — SRE End Term Project

## 1. Automated Deployment Pipeline

### Docker Swarm Deployment
```bash
# Initialize Swarm (once per cluster)
docker swarm init

# Deploy full stack
docker stack deploy -c docker-swarm.yml sre_app

# Rolling update (zero-downtime)
docker service update --image tiangolo/uvicorn-gunicorn-fastapi:python3.10 sre_app_order-service
```

### Kubernetes Deployment
```bash
# Apply all manifests in order
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/database.yaml
kubectl apply -f kubernetes/redis.yaml
kubectl apply -f kubernetes/auth-service.yaml

kubectl apply -f kubernetes/product-service.yaml
kubectl apply -f kubernetes/order-service.yaml
kubectl apply -f kubernetes/payment-service.yaml
kubectl apply -f kubernetes/notification-service.yaml
kubectl apply -f kubernetes/user-profile-service.yaml
kubectl apply -f kubernetes/frontend.yaml
kubectl apply -f kubernetes/monitoring.yaml
```

### Ansible Automation
```bash
# Full environment setup
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml

# Monitoring setup only
ansible-playbook -i ansible/inventory.ini ansible/monitoring.yml

# Kubernetes deployment only
ansible-playbook -i ansible/inventory.ini ansible/kubernetes.yml
```

---

## 2. Health Checks & Restart Policies

### Docker Compose / Swarm
All services define:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 15s
restart: unless-stopped  # or on-failure in Swarm deploy section
```

### Kubernetes
All deployments define both `readinessProbe` and `livenessProbe`:
- **readinessProbe**: prevents traffic until the pod is ready
- **livenessProbe**: restarts the pod if it becomes unresponsive

---

## 3. Capacity Planning

### Resource Consumption Analysis

| Service              | CPU Request | CPU Limit | Memory Request | Memory Limit | Replicas |
|----------------------|-------------|-----------|----------------|--------------|----------|
| auth-service         | 100m        | 250m      | 128Mi          | 256Mi        | 2        |
| product-service      | 100m        | 250m      | 128Mi          | 256Mi        | 2        |
| **order-service**    | **150m**    | **500m**  | **256Mi**      | **512Mi**    | **3**    |
| **payment-service**  | **150m**    | **500m**  | **256Mi**      | **512Mi**    | 2        |
| notification-service | 50m         | 200m      | 64Mi           | 128Mi        | 2        |
| user-profile-service | 100m        | 250m      | 128Mi          | 256Mi        | 2        |
| PostgreSQL           | 250m        | 1000m     | 512Mi          | 1024Mi       | 1        |

**Findings**: Order and Payment services are the most resource-intensive. PostgreSQL is the bottleneck under concurrent load.

### 4. Horizontal Scaling Strategies

#### Docker Swarm Scaling
```bash
# Scale order-service to 5 replicas
docker service scale sre_app_order-service=5

# Scale payment-service
docker service scale sre_app_payment-service=4
```

#### Kubernetes HPA (Horizontal Pod Autoscaler)
The `order-service` and `payment-service` have HPA enabled:
- **Min replicas**: 2
- **Max replicas**: 6 (order) / 5 (payment)
- **Scale trigger**: CPU > 70%

```bash
# Monitor HPA status
kubectl get hpa -n sre-app

# Manual scale
kubectl scale deployment order-service --replicas=5 -n sre-app
```

### 5. Vertical Scaling (Terraform)
Adjust `instance_type` in `terraform/terraform.tfvars`:
```hcl
# Scale up from t2.micro to t3.medium
instance_type = "t3.medium"
```
Then apply:
```bash
cd terraform && terraform apply
```

### 6. Database Optimization
- **Connection Pooling**: Add PgBouncer as a sidecar for connection pooling
- **Indexing**: Add indexes on frequently queried columns
- **Read Replicas**: For read-heavy workloads, configure PostgreSQL streaming replication

---

## 5. Load Simulation
```bash
# Run load simulation script
python3 scripts/simulate_load.py

# Validate service configurations
python3 scripts/validate_config.py

# Health check all services
bash scripts/health_check.sh

# Deploy services with automated checks
bash scripts/deploy.sh
```
