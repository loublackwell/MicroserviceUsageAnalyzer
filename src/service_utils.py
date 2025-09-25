"""
service_utils.py
Author: Lewis Blackwell
Description: Utility functions to handle service names and rates for usage simulation.
Reads services_list.json and allows random selection for simulation.
"""

import json
import random
from pathlib import Path

# Automatically detect project root (assuming this file is in src/)
ROOT_DIR = Path(__file__).parent.parent
SERVICES_FILE = ROOT_DIR / "data/services_list.json"

def load_services() -> list[dict]:
    """
    Load the list of services with their rates from the JSON file.

    Returns:
        List[dict]: List of dictionaries with 'name' and 'rate'.
    """
    if not SERVICES_FILE.exists():
        raise FileNotFoundError(f"Services JSON not found: {SERVICES_FILE}")
    with open(SERVICES_FILE, "r") as f:
        services = json.load(f)
    return services

def get_service_names() -> list[str]:
    """
    Get just the service names from the JSON file.

    Returns:
        List[str]: List of service names.
    """
    return [s["name"] for s in load_services()]

def get_random_services(num: int = 5) -> list[dict]:
    """
    Select a random subset of services with their rates.

    Args:
        num (int): Number of random services to select.

    Returns:
        List[dict]: List of selected service dictionaries with 'name' and 'rate'.
    """
    services = load_services()
    return random.choices(services, k=num)

if __name__ == "__main__":
    print("Available services:", get_service_names())
    print("Randomly selected services:", get_random_services())

