# src/client_logging.py
"""
Client Logging Module
Author: Lewis Blackwell
Purpose: Handles logging for client-side operations, writing messages to logs/client.log
"""

import logging
from pathlib import Path

# ----------------------------
# Setup log folder and file
# ----------------------------
ROOT_DIR = Path(__file__).parent.parent  # project root
LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)  # create logs folder if it doesn't exist

LOG_FILE = LOGS_DIR / "client.log"

# ----------------------------
# Configure logger
# ----------------------------
logger = logging.getLogger("client_logger")
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handler
if not logger.handlers:
    logger.addHandler(file_handler)

# ----------------------------
# Logging utility functions
# ----------------------------
def log_info(message: str):
    """Log an info-level message."""
    logger.info(message)
    print(f"[INFO] {message}")  # also print to console

def log_error(message: str):
    """Log an error-level message."""
    logger.error(message)
    print(f"[ERROR] {message}")  # also print to console

