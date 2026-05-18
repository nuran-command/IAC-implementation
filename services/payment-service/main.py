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

# SRE Velocity Points Cost Settings
COST_PER_POINT = 120  # $120 per complexity story point

@app.get("/")
def root():
    return {"service": "Payment/Cost Estimator", "status": "online", "cost_per_point": COST_PER_POINT}

@app.post("/calculate")
def calculate_cost(payload: dict):
    total_points = payload.get("total_points", 0)
    total_cost = total_points * COST_PER_POINT
    return {
        "status": "success",
        "total_points": total_points,
        "cost_per_point": COST_PER_POINT,
        "total_sprint_cost": f"${total_cost:,}"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return "# HELP payment_service_status Status of payment service\n# TYPE payment_service_status gauge\npayment_service_status 1\n"
