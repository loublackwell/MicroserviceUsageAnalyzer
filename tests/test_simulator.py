"""
PyTest tests for Simulator utility functions
"""

import pytest
from src.simulator import generate_random_usage, random_timestamp

def test_random_timestamp():
    ts = random_timestamp(24)
    assert isinstance(ts, str)

def test_generate_random_usage_structure():
    customers = [{"customer_id": "cust1", "first_name": "Alice"}]
    services = [{"name": "ServiceX", "rate": 10.0}]
    usage_records = generate_random_usage(customers, services)
    assert len(usage_records) > 0
    record = usage_records[0]
    assert "session_id" in record
    assert "customer_id" in record
    assert "service" in record
    assert "units" in record
    assert "price" in record

