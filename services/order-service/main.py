from fastapi import FastAPI
import psycopg2
import os
import time

app = FastAPI()

# Database connection settings retrieved from environment variables
# DB_HOST will be 'db' in your final fixed version
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

@app.get("/")
def read_root():
    """
    Main endpoint that checks database connectivity.
    This logic was used to detect the incident.
    """
    try:
        # Attempting to connect to the PostgreSQL container
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            connect_timeout=3
        )
        conn.close()
        return {
            "status": "online", 
            "message": "Order Service is connected to PostgreSQL"
        }
    except Exception as e:
        # This branch triggered your 'CRITICAL' incident screenshot
        return {
            "status": "error", 
            "message": f"CRITICAL: Database Connection Failed! Error: {str(e)}"
        }

@app.get("/health")
def health_check():
    """Endpoint for Prometheus monitoring"""
    return {"status": "healthy"}