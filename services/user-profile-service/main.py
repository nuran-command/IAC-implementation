from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"service": "User Profile", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP user_profile_service_status Status of user profile service\n# TYPE user_profile_service_status gauge\nuser_profile_service_status 1\n"
