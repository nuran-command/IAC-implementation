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

# Mock SRE Team Members
USERS_DB = [
    {"id": "user-1", "name": "Alice Cooper", "role": "SRE Lead", "initials": "AC", "velocity": "95%"},
    {"id": "user-2", "name": "Bob Marley", "role": "DevSecOps Architect", "initials": "BM", "velocity": "88%"},
    {"id": "user-3", "name": "Charlie Chaplin", "role": "Observability Lead", "initials": "CC", "velocity": "92%"},
    {"id": "user-4", "name": "David Bowie", "role": "Backend Engineer", "initials": "DB", "velocity": "85%"}
]

@app.get("/")
def root():
    return {"service": "Authentication", "status": "online", "users": USERS_DB}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP auth_service_status Status of auth service\n# TYPE auth_service_status gauge\nauth_service_status 1\n"