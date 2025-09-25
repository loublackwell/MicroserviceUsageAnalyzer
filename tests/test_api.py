"""
PyTest tests for FastAPI endpoints using TestClient
"""

import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_record_usage_endpoint():
    payload = {
        "customer_id": "cust_test_api",
        "service": "APIService",
        "units": 5,
        "price": 10.0
    }
    
    response = client.post("/usage", json=payload)  # <-- use json, not params
    data = response.json()
    assert data["status"] == "success"

