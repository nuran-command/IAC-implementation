from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"service": "Notification", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP notification_service_status Status of notification service\n# TYPE notification_service_status gauge\nnotification_service_status 1\n"
