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

# Detailed SRE workloads and active metrics
DEVELOPER_PROFILES = {
    "user-1": {"tasks_in_progress": 1, "tasks_completed": 8, "stress_level": "Low", "on_call": True},
    "user-2": {"tasks_in_progress": 2, "tasks_completed": 5, "stress_level": "Medium", "on_call": False},
    "user-3": {"tasks_in_progress": 0, "tasks_completed": 12, "stress_level": "Low", "on_call": False},
    "user-4": {"tasks_in_progress": 3, "tasks_completed": 4, "stress_level": "High", "on_call": False}
}

@app.get("/")
def root():
    return {"service": "User Profile", "status": "online", "profiles": DEVELOPER_PROFILES}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP user_profile_service_status Status of user profile service\n# TYPE user_profile_service_status gauge\nuser_profile_service_status 1\n"
