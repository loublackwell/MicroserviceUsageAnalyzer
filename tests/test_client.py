# tests/test_client.py
"""
Unit tests for BillingClient.
Tests API connectivity, idempotency, record usage, and retrieval.
"""

import pytest
from src.client import BillingClient

# ------------------------
# Fixtures
# ------------------------
@pytest.fixture
def client():
    # Replace with the actual local/test API URL
    return BillingClient(api_url="http://127.0.0.1:8000")

# ------------------------
# Health Check
# ------------------------
def test_health_check(client):
    """
    Ensure the API server responds to health checks.
    """
    result = client.health_check()
    assert isinstance(result, bool), "Health check should return a boolean"

# ------------------------
# Record Usage
# ------------------------
def test_record_usage(client):
    """
    Test that usage can be recorded.
    """
    response = client.record_usage("test_customer_001", "TestService", 10, 2.5)
    assert isinstance(response, dict)
    assert "error" not in response

# ------------------------
# Idempotency
# ------------------------
def test_idempotent_usage(client):
    """
    Test that duplicate usage submissions are skipped.
    """
    customer_id = "test_customer_002"
    service = "TestService"
    units = 5
    price = 1.0

    first = client.record_usage(customer_id, service, units, price)
    duplicate = client.record_usage(customer_id, service, units, price)

    assert "status" in duplicate
    assert duplicate["status"] == "skipped"

# ------------------------
# Retrieve Usage
# ------------------------
def test_get_usage(client):
    """
    Test retrieval of usage records.
    """
    customer_id = "test_customer_003"
    # record first to ensure something exists
    client.record_usage(customer_id, "TestService", 3, 0.5)
    result = client.get_usage(customer_id)
    assert isinstance(result, dict)

