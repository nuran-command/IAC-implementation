from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"service": "User", "status": "online"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP user_service_status Status of user service\n# TYPE user_service_status gauge\nuser_service_status 1\n"
