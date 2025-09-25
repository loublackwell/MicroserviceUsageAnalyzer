# src/simulator.py
"""
Usage Simulator
Author: Lewis Blackwell
Description: Generates random usage records for customers and inserts them into the database.
Supports realistic duplicates and randomized usage times/units.
Logs important events and errors.
"""

import random
import uuid
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
from src.initialize import InitializeDB
from src.crud import CRUD

# ----------------------------
# Configuration
# ----------------------------
CUSTOMER_SAMPLE_SIZE = 25  # number of unique customers to simulate
USAGE_RECORDS_PER_CUSTOMER = 5  # average number of usage records per customer
UNITS_MIN = 1
UNITS_MAX = 10
UNITS_DECIMALS = 2

ROOT_DIR = Path(__file__).parent.parent
DB_FILE = ROOT_DIR / "customers.db"
SERVICES_JSON = ROOT_DIR / "data/services_list.json"
LOGS_DIR = ROOT_DIR / "logs"

# ----------------------------
# Setup Logger
# ----------------------------
LOGS_DIR.mkdir(exist_ok=True)
logger = logging.getLogger("SimulatorLogger")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGS_DIR / "simulator.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(fh)

# ----------------------------
# Utility Functions
# ----------------------------
def random_timestamp(start_hours_ago=24):
    """Return a random timestamp within the last `start_hours_ago` hours."""
    now = datetime.now()
    delta = timedelta(hours=random.uniform(0, start_hours_ago))
    return (now - delta).strftime("%Y-%m-%d %H:%M:%S")

def cleanup_database():
    """Delete all existing customers and usage records."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usage_records")
        cursor.execute("DELETE FROM customers")
        conn.commit()
        conn.close()
        logger.info("Cleared existing customers and usage records.")
    except Exception as e:
        logger.error(f"Failed to cleanup database: {e}")
        raise

def load_services():
    """Load services and fixed rates from JSON."""
    try:
        with open(SERVICES_JSON, "r") as f:
            services = json.load(f)
        return services
    except Exception as e:
        logger.error(f"Failed to load services: {e}")
        raise

def generate_random_usage(customers, services):
    """Generate random usage records for customers."""
    usage_records = []
    try:
        for _ in range(len(customers) * USAGE_RECORDS_PER_CUSTOMER):
            customer = random.choice(customers)  # allows duplicates
            service = random.choice(services)
            units = round(random.uniform(UNITS_MIN, UNITS_MAX), UNITS_DECIMALS)
            price = round(units * service["rate"], 2)
            usage_records.append({
                "session_id": str(uuid.uuid4()),
                "customer_id": customer["customer_id"],
                "service": service["name"],
                "units": units,
                "price": price,
                "timestamp": random_timestamp()
            })
    except Exception as e:
        logger.error(f"Error generating random usage: {e}")
        raise
    return usage_records

# ----------------------------
# Main Simulator
# ----------------------------
class UsageSimulator:
    """Handles simulation of usage records."""

    def __init__(self, cleanup_db: bool = False):
        try:
            # Optional DB cleanup
            if cleanup_db:
                cleanup_database()

            # Initialize DB and generator
            self.init_db = InitializeDB(root_dir=ROOT_DIR)
            self.init_db.run(rebuild=False)  # do not rebuild unless cleanup

            # Initialize CRUD
            self.crud = CRUD()

            # Load services
            self.services = load_services()

            # Load customers and sample N
            all_customers = self.crud.read_all_customers()
            self.customers = random.sample(all_customers, min(CUSTOMER_SAMPLE_SIZE, len(all_customers)))
        except Exception as e:
            logger.error(f"Simulator initialization failed: {e}")
            raise

    def run(self):
        """Generate random usage and insert into DB."""
        try:
            logger.info(f"Generating usage for {len(self.customers)} customers...")
            usage_records = generate_random_usage(self.customers, self.services)
            for record in usage_records:
                self.crud.create_usage_record(
                    record["session_id"],
                    record["customer_id"],
                    record["service"],
                    record["units"],
                    record["price"]
                )
            logger.info(f"Inserted {len(usage_records)} usage records into the database.")

            # Optional: print first few records for verification
            for record in usage_records[:10]:
                print(record)
        except Exception as e:
            logger.error(f"Failed during simulator run: {e}")
            raise

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    simulator = UsageSimulator(cleanup_db=False)  # default False
    simulator.run()

