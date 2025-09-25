# src/crud.py
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional

DEFAULT_DB_FILE = Path(__file__).parent.parent / "customers.db"

def get_connection(db_file: Path):
    """
    Return a SQLite connection to the specified database with thread safety.
    """
    return sqlite3.connect(db_file, check_same_thread=False)

class CRUD:
    """CRUD operations for customers and usage records."""

    def __init__(self, db_file: Optional[str] = None):
        self.db_file = Path(db_file) if db_file else DEFAULT_DB_FILE
        self.conn = get_connection(self.db_file)
        self.conn.row_factory = sqlite3.Row  # Dict-like rows
        self._ensure_tables()

    def _ensure_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_records (
                session_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                service TEXT NOT NULL,
                units REAL,
                price REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            )
        """)
        self.conn.commit()

    # ----------------- Customer Methods -----------------
    def create_customer(self, customer_id: str, first_name: str):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO customers (customer_id, first_name) VALUES (?, ?)",
            (customer_id, first_name)
        )
        self.conn.commit()

    def read_customer(self, customer_id: str) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def read_all_customers(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers")
        return [dict(r) for r in cursor.fetchall()]

    # ----------------- Usage Methods -----------------
    def create_usage_record(self, session_id: str, customer_id: str,
                            service: str, units: float, price: float):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO usage_records (session_id, customer_id, service, units, price)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, customer_id, service, units, price))
        self.conn.commit()

    def read_usage_records(self, customer_id: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usage_records WHERE customer_id = ?", (customer_id,))
        return [dict(r) for r in cursor.fetchall()]

    def read_all_usage(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usage_records")
        return [dict(r) for r in cursor.fetchall()]

    def update_usage_record(self, session_id: str, **kwargs):
        if not kwargs:
            return
        fields = ", ".join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values()) + [session_id]
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE usage_records SET {fields} WHERE session_id = ?", values)
        self.conn.commit()

    def delete_usage_record(self, session_id: str):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM usage_records WHERE session_id = ?", (session_id,))
        self.conn.commit()

