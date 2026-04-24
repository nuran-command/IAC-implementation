# Infrastructure as Code & SRE Observability Stack

This repository contains the full implementation for **Assignment 4 & 5**. It demonstrates the automated provisioning of cloud infrastructure on AWS using **Terraform** and the deployment of a containerized monitoring stack using **Prometheus, Grafana, and Node Exporter**.

---

## 🚀 Project Overview
The goal of this project is to apply **Site Reliability Engineering (SRE)** principles by:
1. **Provisioning** a high-performance Ubuntu server on AWS EC2.
2. **Automating** network security through Terraform-defined Security Groups.
3. **Deploying** a microservice architecture using Docker Compose.
4. **Establishing Observability** via a professional monitoring pipeline to track SLOs and SLIs.

---

## 🏗 Infrastructure Architecture (Assignment 5)
The infrastructure is defined declaratively in `main.tf`.

* **Cloud Provider:** AWS (Region: us-east-1)
* **Instance Type:** `t3.micro` (Free Tier Eligible)
* **Operating System:** Ubuntu 22.04 LTS
* **Security Group Rules:**
    * **Port 22:** SSH Access for remote management.
    * **Port 80:** Public Web Access (Nginx).
    * **Port 3000:** Grafana Dashboard.
    * **Port 9090:** Prometheus Metrics UI.

---

## 📊 SRE & Monitoring Stack (Assignment 4)
The deployment consists of four interconnected containers:

| Service | Role | Port |
| :--- | :--- | :--- |
| **Nginx** | The primary customer-facing web application. | 80 |
| **Node Exporter** | Collects hardware metrics (CPU, RAM, Disk) from the host. | 9100 |
| **Prometheus** | Time-series database that scrapes and stores metrics. | 9090 |
| **Grafana** | Visualization layer for real-time health monitoring. | 3000 |

---

## 🛠 Deployment Instructions

### 1. Infrastructure Provisioning
Run these commands from your local machine:
```bash
# Initialize Terraform
terraform init

# Plan and Apply
terraform plan
terraform apply -auto-approve
