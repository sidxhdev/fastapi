
# Inventory Manager

A full-stack inventory management system built with FastAPI, React, and PostgreSQL, deployed on AWS with a Jenkins CI/CD pipeline.

## Live Demo

- Frontend: https://inventory-manager.sidxh.com
- Backend API: https://api.inventory-manager.sidxh.com
- API Docs: https://api.inventory-manager.sidxh.com/docs

---

## Tech Stack

### Backend
- FastAPI
- PostgreSQL (AWS RDS)
- Redis (caching)
- SQLAlchemy
- psycopg2-binary

### Frontend
- React
- Axios

### Infrastructure
- AWS EC2 (backend server)
- AWS S3 (frontend hosting)
- AWS RDS (PostgreSQL database)
- Nginx (reverse proxy + SSL termination)
- Let's Encrypt (SSL certificates)
- Docker + Docker Compose
- Jenkins (CI/CD pipeline)

---

## Project Structure

```
fastapi/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── App.css
│   └── public/
│       └── index.html
├── docker-compose.yml
├── Jenkinsfile
└── requirements.txt
```

---

## Setup

### Prerequisites

- Docker
- Node.js
- Python 3.12
- AWS account

### Environment Variables

```
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/inventory_db
REDIS_HOST=redis
REDIS_PORT=6379
ENVIRONMENT=production
```

### Run Locally

```bash
# clone the repo
git clone https://github.com/sidxhdev/fastapi
cd fastapi

# start backend + redis
docker compose up -d

# start frontend
cd frontend
npm install
npm start
```

---

## CI/CD Pipeline

Every push to `master` triggers the Jenkins pipeline:

1. Checkout code from GitHub
2. Build backend Docker image
3. Start backend + Redis via Docker Compose
4. Build React frontend
5. Deploy frontend build to AWS S3

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /products/ | Get all products |
| GET | /products/{id} | Get product by ID |
| POST | /products/ | Add a new product |
| PUT | /products/{id} | Update a product |
| DELETE | /products/{id} | Delete a product |

---

## Architecture

```
Browser
  |
  |-- https://inventory-manager.sidxh.com  (S3 via Nginx)
  |-- https://api.inventory-manager.sidxh.com  (FastAPI via Nginx)
        |
        |-- PostgreSQL (AWS RDS)
        |-- Redis (cache)
```

---

## Author

Siddesh Navthale

- GitHub: https://github.com/sidxhdev
- Blog: https://siddeshblogs.hashnode.dev