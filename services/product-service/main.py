from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/")
def root():
    return {"service": "Product", "items": ["Laptop", "Monitor", "Keyboard"], "status": "online"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP product_service_status Status of product service\n# TYPE product_service_status gauge\nproduct_service_status 1\n"