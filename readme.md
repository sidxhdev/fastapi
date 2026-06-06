# Cloud-Native Inventory Management System

## Overview

A full-stack cloud-native Inventory Management System built using FastAPI, React, PostgreSQL, Redis, Docker, Kubernetes, Jenkins, GitHub Actions, and AWS.

The application enables users to manage inventory products through a modern web interface while demonstrating industry-standard DevOps practices such as containerization, CI/CD, cloud deployment, monitoring, and caching.

---

## Architecture

```text
Users
  |
  v
CloudFront
  |
  v
S3 (React Frontend)
  |
  v
AWS Load Balancer
  |
  v
Kubernetes (EKS)
  |
  +--> FastAPI Pods
  |
  +--> FastAPI Pods
  |
  +--> Redis Cache
  |
  +--> RDS PostgreSQL

Monitoring Stack
  |
  +--> Prometheus
  +--> Grafana
  +--> Loki

CI/CD Pipeline
  |
  +--> GitHub Actions
  +--> Jenkins
  +--> Docker
  +--> ECR
  +--> EKS
```

---

## Features

* Product Inventory CRUD Operations
* PostgreSQL Database Integration
* Redis-Based Caching Layer
* RESTful APIs with FastAPI
* React Frontend with Responsive UI
* Dockerized Services
* Kubernetes Deployment
* Automated CI/CD Pipelines
* Monitoring and Alerting
* Cloud Deployment on AWS

---

## Tech Stack

### Frontend

* React
* Vite
* Axios
* Tailwind CSS

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis
* Pydantic

### DevOps

* Docker
* Kubernetes
* Jenkins
* GitHub Actions

### Monitoring

* Prometheus
* Grafana
* Loki
* Promtail

### Cloud

* AWS EC2
* AWS S3
* AWS CloudFront
* AWS RDS
* AWS ECR
* AWS EKS

---

## Project Structure

```text
inventory-management/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── Dockerfile
│
├── backend/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── database.py
│   ├── main.py
│   └── Dockerfile
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── configmap.yaml
│
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── loki/
│
├── Jenkinsfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## CI/CD Workflow

### GitHub Actions

* Run code quality checks
* Execute backend tests
* Build Docker images
* Push images to Amazon ECR

### Jenkins

* Triggered through GitHub Webhooks
* Pull latest container image
* Deploy to Kubernetes Cluster
* Perform rolling updates

Pipeline Flow:

```text
GitHub
   |
   v
GitHub Actions
   |
   v
Amazon ECR
   |
   v
Jenkins
   |
   v
Amazon EKS
```

---

## Monitoring

### Prometheus

Collects:

* API Request Count
* API Latency
* CPU Usage
* Memory Usage
* Pod Health Metrics

### Grafana

Dashboards:

* Application Metrics
* Infrastructure Metrics
* Kubernetes Metrics
* Database Performance

### Loki

Centralized Log Aggregation:

* FastAPI Logs
* Kubernetes Logs
* Application Errors

---

## Caching Strategy

Redis is used for:

* Frequently accessed product data
* API response caching
* Session storage
* Rate limiting

Benefits:

* Reduced database load
* Faster API responses
* Improved scalability

---

## Deployment

### Frontend

Hosted using:

* AWS S3
* AWS CloudFront

### Backend

Hosted on:

* Amazon EKS

### Database

Managed using:

* Amazon RDS PostgreSQL

### Container Registry

* Amazon ECR

---

## Security

* Kubernetes Secrets
* AWS IAM Roles
* Security Groups
* HTTPS via Load Balancer
* Environment Variable Management

---

## Future Improvements

* Terraform Infrastructure as Code
* Blue-Green Deployments
* Canary Releases
* Distributed Tracing
* Multi-Region Deployment
* Automated Disaster Recovery

---

## Learning Outcomes

This project demonstrates practical experience with:

* Backend Development
* Cloud Computing
* Containerization
* Kubernetes
* CI/CD Automation
* Monitoring and Observability
* Caching Strategies
* AWS Infrastructure

