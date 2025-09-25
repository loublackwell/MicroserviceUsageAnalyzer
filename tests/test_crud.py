# tests/test_crud.py
import pytest
from src.crud import CRUD

TEST_DB_FILE = "test_customers.db"

@pytest.fixture
def crud():
    db = CRUD(db_file=TEST_DB_FILE)
    yield db
    # No need to call db.close() because check_same_thread=False allows thread-safe use

def test_create_and_read_customer(crud):
    crud.create_customer("cust_test", "John")
    customer = crud.read_customer("cust_test")
    assert customer is not None
    assert customer["customer_id"] == "cust_test"
    assert customer["first_name"] == "John"

def test_create_and_read_usage(crud):
    crud.create_customer("cust_test2", "Alice")
    crud.create_usage_record("sess_test", "cust_test2", "APIService", 10, 50.0)
    records = crud.read_usage_records("cust_test2")
    assert len(records) == 1
    record = records[0]
    assert record["session_id"] == "sess_test"
    assert record["customer_id"] == "cust_test2"
    assert record["service"] == "APIService"
    assert record["units"] == 10
    assert record["price"] == 50.0

