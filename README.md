# End-Term SRE Project
## End-to-End SRE Implementation — Distributed Microservices System

> **Technologies**: Docker Swarm · Kubernetes · Terraform · Ansible · Prometheus · Grafana

---

## 1. System Architecture

```
User
 │
 ▼
Frontend (Nginx)
 │
 ▼
API Gateway
 │
 ├── auth-service         (Auth & Security)
 ├── product-service      (Product Catalog)
 ├── order-service        (Order Processing)   ← Incident Service
 ├── payment-service      (Payment Simulation)
 ├── notification-service (Email/Alert Sim)
 └── user-profile-service (User Data)
          │
     PostgreSQL / Redis
          │
Monitoring: Prometheus → Grafana
Infrastructure: Terraform → AWS EC2
Configuration: Ansible → Docker + Kubernetes Setup
Orchestration: Docker Swarm + Kubernetes
```

---

## 2. Project Structure

```
endterm-sre/
├── services/                       # Assignment 1, 4 — Microservices source code
│   ├── auth-service/
│   ├── product-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── notification-service/
│   └── user-profile-service/
├── frontend/                       # Nginx-based web interface
├── docker-compose.yml              # Assignment 1 — Local dev orchestration
├── docker-swarm.yml                # Assignment 1, 6 — Docker Swarm stack (deploy sections)
├── kubernetes/                     # Assignment 6 — Per-microservice K8s manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── database.yaml               # PostgreSQL StatefulSet + PVC
│   ├── redis.yaml                  # Redis Message Broker
│   ├── auth-service.yaml           # Deployment + Service

│   ├── product-service.yaml        # Deployment + Service
│   ├── order-service.yaml          # Deployment + Service + HPA
│   ├── payment-service.yaml        # Deployment + Service + HPA
│   ├── notification-service.yaml   # Deployment + Service
│   ├── user-profile-service.yaml   # Deployment + Service
│   ├── frontend.yaml               # Nginx Deployment + NodePort Service
│   └── monitoring.yaml             # Prometheus + Grafana + RBAC
├── terraform/                      # Assignment 5 — Infrastructure as Code
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars
├── ansible/                        # Assignment 5, 6 — Configuration Management
│   ├── inventory.ini
│   ├── playbook.yml                # Full environment setup
│   ├── monitoring.yml              # Monitoring stack setup
│   └── kubernetes.yml              # K8s manifests deployment
├── monitoring/                     # Assignment 3 — Observability
│   ├── prometheus.yml
│   ├── alert_rules.yml
│   └── grafana-dashboard.json
├── scripts/                        # Assignment 6 — Automation
│   ├── deploy.sh                   # Automated deployment (swarm|kubernetes)
│   ├── health_check.sh             # Service health validation
│   ├── incident_simulate.sh        # Incident injection & recovery
│   ├── simulate_load.py            # Load generation
│   └── validate_config.py          # Config validation
├── docs/                           # Documentation
│   ├── SLI_SLO.md                  # Assignment 2 — SLI/SLO definitions
│   ├── INCIDENT_POSTMORTEM.md      # Assignment 4 — Postmortem
│   ├── CAPACITY_PLANNING.md        # Assignment 6 — Capacity planning
│   └── AUTOMATION.md               # Assignment 6 — Automation guide
├── nginx.conf
├── .env.example
└── README.md
```

---

## 3. SLI/SLO Summary (Assignment 2)

| SLI            | SLO Target |
|----------------|-----------|
| Availability   | ≥ 99%     |
| Latency (p95)  | ≤ 200 ms  |
| Error Rate     | ≤ 1%      |
| Success Rate   | ≥ 99%     |

See full definitions: [`docs/SLI_SLO.md`](docs/SLI_SLO.md)

---

## 4. Quick Start

### Option A — Docker Swarm
```bash
# Initialize and deploy
docker swarm init
docker stack deploy -c docker-swarm.yml sre_app

# Or use the automation script
bash scripts/deploy.sh swarm
```

### Option B — Docker Compose (local dev)
```bash
cp .env.example .env
docker compose up -d
```

### Option C — Kubernetes
```bash
bash scripts/deploy.sh kubernetes
```

### Option D — Ansible (full automation)
```bash
# Edit ansible/inventory.ini with your server IPs first
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

---

## 5. Monitoring Access

| Tool       | URL (Swarm)                  | URL (Kubernetes)             |
|------------|------------------------------|------------------------------|
| Frontend   | http://localhost:80           | http://localhost:30080       |
| Prometheus | http://localhost:9090         | http://localhost:30090       |
| Grafana    | http://localhost:3000 (admin/admin) | http://localhost:30300 |

Import `monitoring/grafana-dashboard.json` to Grafana for the pre-built dashboard.

---

## 6. Incident Simulation (Assignment 4)

```bash
# Inject failure (wrong DB_HOST → crash loop)
bash scripts/incident_simulate.sh inject

# Monitor in Prometheus: order_service_status == 0
# Check logs: docker service logs sre_app_order-service

# Recover
bash scripts/incident_simulate.sh recover
```

See full postmortem: [`docs/INCIDENT_POSTMORTEM.md`](docs/INCIDENT_POSTMORTEM.md)

---

## 7. Infrastructure (Assignment 5)

```bash
# Provision AWS EC2 instance
cd terraform
terraform init
terraform plan
terraform apply
```

---

## 8. Health Checks & Automation Scripts

```bash
# Verify the health of all 6 microservices
bash scripts/health_check.sh

# Run pytest unit tests across all microservices
pytest services/
```

---

## 9. Team Workflow & CI/CD Pipeline (Team Final Upgrade)

This project has been expanded for enterprise team collaboration:
1. **Team Collaboration**: Detailed roles, branching models, and SRE PR review gates are defined in [`docs/TEAM_WORKFLOW.md`](docs/TEAM_WORKFLOW.md).
2. **CI/CD Pipeline**: A comprehensive GitHub Actions workflow at [`.github/workflows/cicd.yml`](.github/workflows/cicd.yml) automates linting, validation (Terraform, Ansible, Kubernetes Configs), pytest unit testing, Docker stack compiling, and delivery verification.

---

## Assignment Coverage Checklist

- [x] **Assignment 1** — Docker setup, 6 microservices, Docker Compose
- [x] **Assignment 2** — SLI/SLO definitions (`docs/SLI_SLO.md`)
- [x] **Assignment 3** — Prometheus + Grafana + Alert rules
- [x] **Midterm**     — Functional microservices deployment
- [x] **Assignment 4** — Incident simulation, postmortem (`docs/INCIDENT_POSTMORTEM.md`)
- [x] **Assignment 5** — Terraform IaC + Ansible configuration management
- [x] **Assignment 6** — Automation scripts (`scripts/deploy.sh`, `scripts/health_check.sh`, `scripts/incident_simulate.sh`), Docker Swarm, Kubernetes manifests, capacity planning (`docs/CAPACITY_PLANNING.md`)
- [x] **Final Upgrade** — Team Collaboration Guide (`docs/TEAM_WORKFLOW.md`) & Automated CI/CD Pipeline (`.github/workflows/cicd.yml`) with pytest unit test suites.
