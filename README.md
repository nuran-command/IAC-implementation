# Infrastructure as Code & SRE Observability Stack

This repository contains the full implementation for **Assignment 4 & 5**. It demonstrates the automated provisioning of cloud infrastructure on **AWS** using **Terraform** and the deployment of a containerized monitoring stack using **Prometheus** and **Grafana**.

---

## **Project Overview**

The goal of this project is to apply **Site Reliability Engineering (SRE)** principles:

* **Provisioning:** High-performance Ubuntu server on **AWS EC2**.
* **Automation:** Network security defined via **Terraform Security Groups**.
* **Deployment:** Multi-tier microservice architecture using **Docker Compose**.
* **Observability:** Establishing a monitoring pipeline to track service health and connectivity.

---

## **Infrastructure Architecture (Assignment 5)**

The infrastructure is defined declaratively in `main.tf`.

* **Cloud Provider:** AWS (Region: `us-east-1`)
* **Instance Type:** `t3.micro`
* **Operating System:** `Ubuntu 22.04 LTS`
* **Security Group Rules:**
  * **Port 22:** SSH Access for remote management.
  * **Port 80:** Public Web Access (Order Service / API).
  * **Port 8080:** Frontend Access (Nginx).
  * **Port 9090:** Prometheus Metrics UI.
  * **Port 3000:** Grafana Dashboard.

---

## **SRE & Monitoring Stack (Assignment 4)**

The deployment consists of five interconnected containers:

| Service | Role | Port |
| :--- | :--- | :--- |
| **Order Service** | FastAPI backend handling business logic. | `80` |
| **PostgreSQL** | Persistent database for order storage. | `5432` |
| **Nginx** | Static frontend layer. | `8080` |
| **Prometheus** | Time-series DB that scrapes service health. | `9090` |
| **Grafana** | Visualization layer for real-time monitoring. | `3000` |

---

## **Incident Response Simulation**

This project simulates a **High-Severity Production Incident**:

* **The Incident:** `order-service` failed with `CRITICAL: Database Connection Failed!`.
* **Root Cause:** Misconfigured `DB_HOST` environment variable.
* **The Mitigation:**
  * Corrected internal DNS resolution in `docker-compose.yml`.
  * Implemented a `restart: always` policy for service resilience.
* **Recovery:** Verified status restoration to `{"status": "online"}`.

---

## **Deployment Instructions**

### **1. Infrastructure Provisioning**

Run from your local terminal:

```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply and provision resources
terraform apply -auto-approve

## **2. Service Deployment**

```bash
# Deploy the monitoring stack using Docker Compose
docker compose up -d

# Navigate to project directory
cd ~/IAC-implementation

# Deploy the stack
sudo docker compose up -d
```
