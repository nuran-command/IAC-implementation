from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"service": "Chat", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP chat_service_status Status of chat service\n# TYPE chat_service_status gauge\nchat_service_status 1\n"