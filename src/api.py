"""
api.py
Author: Lewis Blackwell
Goal: Provide internal web service API to record and read usage data.
"""

import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from src.crud import CRUD

app = FastAPI()
crud = CRUD()

# ----------------------------
# Pydantic Models
# ----------------------------
class UsageRecord(BaseModel):
    session_id: str | None = None  # optional, will generate if not provided
    customer_id: str
    service: str
    units: float
    price: float

# ----------------------------
# API Endpoints
# ----------------------------
@app.post("/usage")
def record_usage(record: UsageRecord):
    """
    Record a usage entry in the database.

    Args:
        record (UsageRecord): The usage record data in JSON format.
        
    Returns:
        dict: Status message confirming the record insertion.
    """
    session_id = record.session_id or str(uuid.uuid4())
    crud.create_usage_record(
        session_id=session_id,
        customer_id=record.customer_id,
        service=record.service,
        units=record.units,
        price=record.price
    )
    return {"status": "success", "message": "Usage recorded.", "session_id": session_id}


@app.get("/health")
def health_check():
    """
    Simple health check endpoint to verify the API is running.
    
    Returns:
        dict: Status message indicating the service is healthy.
    """
    return {"status": "healthy"}


# ----------------------------
# Run locally for testing
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

