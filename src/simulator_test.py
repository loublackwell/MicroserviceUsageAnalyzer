"""
simulator_test.py
Author: Lewis Blackwell
Goal: Simulate and test CRUD operations and API-like interactions for usage records.
      Uses a separate test database to avoid affecting production data.
"""

import uuid
import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from src.crud import CRUD


# ----------------------------
# Configuration
# ----------------------------
ROOT_DIR = Path(__file__).parent.parent
TEST_DB_FILE = ROOT_DIR / "customers_test.db"
CUSTOMER_SAMPLE_SIZE = 5
USAGE_RECORDS_PER_CUSTOMER = 3


# ----------------------------
# Utility Functions
# ----------------------------
def random_timestamp(start_hours_ago=24):
    """Return a random timestamp within the last `start_hours_ago` hours."""
    now = datetime.now()
    delta = timedelta(hours=random.uniform(0, start_hours_ago))
    return (now - delta).strftime("%Y-%m-%d %H:%M:%S")


# ----------------------------
# Simulator Test Class
# ----------------------------
class SimulatorTest:
    """Class to simulate and test usage records in a separate database."""

    def __init__(self):
        """
        Initialize CRUD instance with test database.
        Creates tables if they do not exist.
        """
        self.crud = CRUD(db_file=TEST_DB_FILE)
        self._ensure_test_customers()

    def _ensure_test_customers(self):
        """Populate test database with sample customers if empty."""
        existing = self.crud.read_all_customers()
        if len(existing) < CUSTOMER_SAMPLE_SIZE:
            for i in range(CUSTOMER_SAMPLE_SIZE):
                customer_id = f"test_cust_{i}"
                self.crud.create_customer(customer_id, f"TestUser{i}")
        self.customers = self.crud.read_all_customers()

    # ----------------------------
    # Test Methods
    # ----------------------------
    def test_normal_usage(self):
        """Insert normal usage records."""
        print("[TEST] Normal usage insertion")
        for customer in self.customers:
            for _ in range(USAGE_RECORDS_PER_CUSTOMER):
                self.crud.create_usage_record(
                    session_id=str(uuid.uuid4()),
                    customer_id=customer["customer_id"],
                    service="TestService",
                    units=round(random.uniform(1, 5), 2),
                    price=round(random.uniform(0.1, 10.0), 2)
                )

    def test_duplicate_session_id(self):
        """Attempt to insert duplicate session IDs to test constraints."""
        print("[TEST] Duplicate session ID insertion")
        session_id = str(uuid.uuid4())
        customer = self.customers[0]
        self.crud.create_usage_record(session_id, customer["customer_id"], "TestService", 1.0, 1.0)
        try:
            # Should be ignored or fail gracefully
            self.crud.create_usage_record(session_id, customer["customer_id"], "TestService", 2.0, 2.0)
        except Exception as e:
            print(f"Caught expected duplicate error: {e}")

    def test_invalid_data(self):
        """Attempt to insert invalid data (missing fields) and observe behavior."""
        print("[TEST] Invalid data insertion")
        try:
            # Missing service
            self.crud.create_usage_record(str(uuid.uuid4()), self.customers[0]["customer_id"], None, 1.0, 1.0)
        except Exception as e:
            print(f"Caught expected invalid data error: {e}")

    def test_cleanup(self):
        """Clean up test database records."""
        print("[TEST] Cleaning up test database")
        for record in self.crud.read_all_usage():
            self.crud.delete_usage_record(record["session_id"])
        for customer in self.customers:
            self.crud.create_customer(customer["customer_id"], customer["first_name"])  # reset customers


# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    simulator_test = SimulatorTest()
    simulator_test.test_normal_usage()
    simulator_test.test_duplicate_session_id()
    simulator_test.test_invalid_data()
    # Optional cleanup after tests
    simulator_test.test_cleanup()
    print("[TEST] Simulator testing complete.")

