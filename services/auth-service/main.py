from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"service": "Authentication", "status": "online"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP auth_service_status Status of auth service\n# TYPE auth_service_status gauge\nauth_service_status 1\n"