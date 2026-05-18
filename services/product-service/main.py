from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standard Product Backlog Items
BACKLOG_TASKS = [
    {
        "id": "task-1",
        "title": "Configure Prometheus alert rules",
        "desc": "Set up alerts for high CPU usage and low memory on the host swarm nodes.",
        "priority": "High",
        "points": 5,
        "column": "backlog"
    },
    {
        "id": "task-2",
        "title": "Optimize Postgres indexes",
        "desc": "Analyze query performance and add missing indexes for user transactions.",
        "priority": "Medium",
        "points": 3,
        "column": "backlog"
    },
    {
        "id": "task-3",
        "title": "Document disaster recovery playbook",
        "desc": "Create a step-by-step incident response playbook in docs/ for on-call engineers.",
        "priority": "Low",
        "points": 2,
        "column": "todo"
    },
    {
        "id": "task-4",
        "title": "Refactor API Gateway rewrite rules",
        "desc": "Ensure Nginx correctly forwards requests to the newly registered endpoints.",
        "priority": "High",
        "points": 8,
        "column": "todo"
    }
]

@app.get("/")
def root():
    return {"service": "Product Catalog", "status": "online", "tasks": BACKLOG_TASKS}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP product_service_status Status of product service\n# TYPE product_service_status gauge\nproduct_service_status 1\n"