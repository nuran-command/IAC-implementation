# Infrastructure as Code & SRE Automation Stack

This repository contains the full implementation for **Assignments 4, 5, and 6**. It demonstrates the evolution from a microservices system with basic monitoring to a highly automated, resilient, and scalable architecture following SRE principles.

---

## **Assignment 6: Automation & Capacity Planning**

This phase focuses on reducing operational toil and preparing the system for high load.

### **1. Automation Mechanisms**
- **Self-Healing Infrastructure**: Every service now includes Docker health checks and `unless-stopped` restart policies.
- **Monitoring-Based Alerting**: Prometheus is configured with rules to alert on service downtime, high CPU usage, and application-level errors.
- **Automated Configuration Validation**: A `validate_config.py` script ensures that environment variables are correctly set before deployment, preventing the misconfiguration incident seen in Assignment 4.

### **2. Capacity Planning & Scaling**
- **Load Simulation**: A `simulate_load.py` script enables stress-testing the system by generating concurrent API requests.
- **Horizontal Scaling**: The `order-service` is now load-balanced across multiple instances via Nginx `upstream` configuration.
- **Vertical Scaling**: Terraform infrastructure is parameterized to allow seamless upgrades of instance types (e.g., from `t3.micro` to `t3.small`).

---

## **Deployment & Automation Workflow**

### **1. Validation**
Before deploying, validate the environment configuration:
```bash
python3 validate_config.py
```

### **2. Infrastructure Provisioning (Terraform)**
```bash
terraform init
terraform apply -var="instance_type=t3.small" # Example of vertical scaling
```

### **3. Service Deployment (Docker Compose)**
```bash
docker-compose up -d --build
```

### **4. Load Testing**
```bash
python3 simulate_load.py
```

---

## **SRE Monitoring Stack**

| Service | Role | Port |
| :--- | :--- | :--- |
| **Frontend** | Nginx-based static web interface. | `8080` |
| **Auth Service** | FastAPI Authentication handler. | `80` |
| **Order Service** | FastAPI (Load Balanced x2) | `80` |
| **Prometheus** | Time-series DB with alerting rules. | `9090` |
| **Grafana** | Real-time observability dashboards. | `3002` |
