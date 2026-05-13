from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"service": "Payment", "status": "online"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP payment_service_status Status of payment service\n# TYPE payment_service_status gauge\npayment_service_status 1\n"
