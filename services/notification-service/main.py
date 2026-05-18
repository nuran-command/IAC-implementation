from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Shared memory log list
ACTIVITY_LOGS = [
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "event": "SRE board initialized.", "severity": "info"},
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "event": "Alice Cooper went on-call.", "severity": "warning"},
    {"timestamp": datetime.now().strftime("%H:%M:%S"), "event": "Bob Marley moved task-6 to Done.", "severity": "success"}
]

@app.get("/")
def root():
    return {"service": "Notification Hub", "status": "online", "logs": ACTIVITY_LOGS}

@app.post("/log")
def add_log(payload: dict):
    event = payload.get("event")
    severity = payload.get("severity", "info")
    if event:
        ACTIVITY_LOGS.insert(0, {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "event": event,
            "severity": severity
        })
        # Keep logs list clean (max 15 items)
        if len(ACTIVITY_LOGS) > 15:
            ACTIVITY_LOGS.pop()
    return {"status": "success", "count": len(ACTIVITY_LOGS)}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP notification_service_status Status of notification service\n# TYPE notification_service_status gauge\nnotification_service_status 1\n"
