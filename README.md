# End-to-End Implementation of Site Reliability Engineering Practices

## Abstract
This project presents a comprehensive implementation of Site Reliability Engineering (SRE) principles applied to a distributed microservices-based system. The system integrates containerization, multi-platform orchestration (Docker Swarm and Kubernetes), monitoring, infrastructure provisioning (Terraform), configuration management (Ansible), incident response, and capacity planning.

## System Overview
The architecture consists of 6 independent microservices:
1. **Auth Service** — user login and security
2. **Product Service** — product catalog management
3. **Order Service** — order processing
4. **Payment Service** — payment handling simulation
5. **Notification Service** — email/alert simulation
6. **User Profile Service** — user data management

### Supporting Components
- **Frontend**: Nginx-based web interface and reverse proxy.
- **Database**: PostgreSQL
- **Monitoring**: Prometheus + Grafana

## Project Structure
```text
├── ansible/               # Ansible configuration management playbooks
├── docs/                  # SRE documentation (Postmortem, Capacity Planning)
├── frontend/              # Nginx frontend application
├── kubernetes/            # Kubernetes deployment manifests
├── monitoring/            # Prometheus configuration and alert rules
├── scripts/               # Validation and load simulation scripts
├── services/              # Microservice source code (FastAPI)
│   ├── auth-service/
│   ├── notification-service/
│   ├── order-service/
│   ├── payment-service/
│   ├── product-service/
│   └── user-profile-service/
├── terraform/             # Terraform infrastructure provisioning
├── docker-compose.yml     # Docker Swarm orchestration
└── nginx.conf             # API Gateway configuration
```

## Setup & Deployment

### 1. Infrastructure Provisioning (Terraform)
Provision AWS infrastructure using Terraform:
```bash
cd terraform
terraform init
terraform apply
```

### 2. Configuration Management (Ansible)
Run Ansible to install Docker/Kubernetes and deploy the stack:
```bash
cd ansible
ansible-playbook -i inventory playbook.yml
```

### 3. Orchestration 

#### Option A: Docker Swarm
```bash
docker swarm init
docker stack deploy -c docker-compose.yml sre_app
```

#### Option B: Kubernetes
```bash
kubectl apply -f kubernetes/app-deployment.yaml
```

## SRE Practices Implemented
- **Multi-Orchestration**: Kubernetes and Docker Swarm are used to demonstrate declarative vs basic clustering strategies.
- **Infrastructure as Code**: Cloud environments are bootstrapped cleanly and repeatably with Terraform.
- **Configuration Management**: Ansible automates software dependencies and application rollouts.
- **Observability**: Prometheus collects `/metrics` from all 6 services. Grafana visualizes the uptime, request rates, and resource utilization.
- **Incident Response**: `docs/INCIDENT_POSTMORTEM.md` covers a simulated root-cause analysis of an `order-service` database configuration failure.
- **Capacity Planning**: `docs/CAPACITY_PLANNING.md` defines scaling strategies (horizontal/vertical) to address load constraints in the database and intensive API endpoints.
