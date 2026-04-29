from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

@app.get("/")
def root():
    db_host = os.getenv("DB_HOST", "db")
    if db_host == "db_wrong":
        return {"service": "Order", "status": "offline", "error": "Database connection failed"}
    return {"service": "Order", "status": "online"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    db_host = os.getenv("DB_HOST", "db")
    if db_host == "db_wrong":
        return "# HELP order_service_status Status of order service\n# TYPE order_service_status gauge\norder_service_status 0\n"
    return "# HELP order_service_status Status of order service\n# TYPE order_service_status gauge\norder_service_status 1\n"