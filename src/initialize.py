"""
initialize.py
Author: Lewis Blackwell
Description: Initializes the database using customer data generated
by the Generator class. Tracks status in a JSON file to avoid duplicate initialization.
Automatically detects project root so CSV is always found.
"""

import argparse
import json
import sqlite3
from pathlib import Path
from src.generator import Generator  # import your existing CSV -> UUID generator

class InitializeDB:
    """
    Handles database initialization and mock data generation.
    """

    def __init__(self, root_dir: str = None, db_file: str = "customers.db", status_file: str = "status.json"):
        # Automatically detect root_dir if not provided
        if root_dir:
            self.root_dir = Path(root_dir)
        else:
            # Same logic as generator.py: assume this file is in src/ and root is parent
            self.root_dir = Path(__file__).parent.parent

        self.db_file = self.root_dir / db_file
        self.status_file = self.root_dir / status_file
        self.status = self.read_status()

        # Initialize Generator with correct root_dir
        self.generator = Generator(root_dir=self.root_dir)

    # ----------------------------
    # Status helpers
    # ----------------------------
    def read_status(self):
        if self.status_file.exists():
            with open(self.status_file, "r") as f:
                return json.load(f)
        return {"mock_data_generated": False, "db_initialized": False}

    def write_status(self):
        with open(self.status_file, "w") as f:
            json.dump(self.status, f, indent=2)

    # ----------------------------
    # Generate mock data
    # ----------------------------
    def generate_mock_data(self):
        """Generates customer data using the Generator class."""
        print("[initialize] Generating customer data from CSV...")
        customers = self.generator.generate_customers()
        self.status["mock_data_generated"] = True
        return customers

    # ----------------------------
    # Database initialization
    # ----------------------------
    def initialize_database(self, customers):
        """Creates SQLite database and inserts customer data."""
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL
            )
        """)

        # Insert customer data
        cur.executemany(
            "INSERT OR IGNORE INTO customers (customer_id, first_name) VALUES (?, ?)",
            [(c["customer_id"], c["first_name"]) for c in customers]
        )

        conn.commit()
        conn.close()
        self.status["db_initialized"] = True
        print(f"[initialize] Database initialized with {len(customers)} customers.")

    # ----------------------------
    # Orchestration
    # ----------------------------
    def run(self, rebuild: bool = False):
        """Runs the initialization process."""
        if rebuild:
            print("[initialize] Rebuild requested. Removing database and status file if present.")
            if self.db_file.exists():
                self.db_file.unlink()
            self.status = {"mock_data_generated": False, "db_initialized": False}

        # Generate mock data if not already done
        customers = []
        if not self.status["mock_data_generated"]:
            customers = self.generate_mock_data()
        else:
            print("[initialize] Mock data already generated. Skipping.")

        # Initialize database if not already done
        if not self.status["db_initialized"]:
            if not customers:  # regenerate if needed
                customers = self.generator.generate_customers()
            self.initialize_database(customers)
        else:
            print("[initialize] Database already initialized. Skipping.")

        # Write status to file
        self.write_status()


# ----------------------------
# CLI entrypoint
# ----------------------------
def main():
    parser = argparse.ArgumentParser(description="Initialize database and customer data.")
    parser.add_argument("--root-dir", default=None, help="Project root directory (optional)")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild database and regenerate data")
    args = parser.parse_args()

    init = InitializeDB(root_dir=args.root_dir)
    init.run(rebuild=args.rebuild)


if __name__ == "__main__":
    main()

