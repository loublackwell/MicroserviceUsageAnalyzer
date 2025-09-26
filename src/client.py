# src/client.py
"""
Client Library
Author: Lewis Blackwell
Purpose: Provides a client interface to interact with the internal usage tracking API.
Includes retry logic, idempotent usage tracking, and health check support.
"""

import requests
from typing import Optional
from time import sleep
from .client_logging import log_info, log_error


class BillingClient:
    """
    Client class to interact with the internal usage tracking API.

    Attributes:
        api_url (str): Base URL of the internal API.
        max_retries (int): Maximum number of retries for failed requests.
        backoff_factor (float): Multiplier for exponential backoff between retries.
    """

    def __init__(self, api_url: str, max_retries: int = 3, backoff_factor: float = 2.0):
        self.api_url = api_url.rstrip("/")
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._submitted_usages = set()  # Track submissions for idempotency
        log_info(f"BillingClient initialized with API URL: {self.api_url}")

    def _post_with_retry(self, endpoint: str, payload: dict):
        """
        Internal helper to send POST requests with retry logic and exponential backoff.
        """
        delay = 1
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(f"{self.api_url}/{endpoint}", json=payload)
                response.raise_for_status()
                log_info(f"Successfully sent POST to {endpoint} on attempt {attempt}")
                return response.json()
            except requests.RequestException as e:
                log_error(f"Attempt {attempt} failed for {endpoint}: {e}")
                if attempt < self.max_retries:
                    sleep(delay)
                    delay *= self.backoff_factor
                else:
                    log_error(f"All {self.max_retries} attempts failed for {endpoint}")
                    return {"error": str(e)}

    def _get_with_retry(self, endpoint: str):
        """
        Internal helper to send GET requests with retry logic and exponential backoff.
        """
        delay = 1
        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(f"{self.api_url}/{endpoint}")
                response.raise_for_status()
                log_info(f"Successfully retrieved GET from {endpoint} on attempt {attempt}")
                return response.json()
            except requests.RequestException as e:
                log_error(f"Attempt {attempt} failed for GET {endpoint}: {e}")
                if attempt < self.max_retries:
                    sleep(delay)
                    delay *= self.backoff_factor
                else:
                    log_error(f"All {self.max_retries} attempts failed for GET {endpoint}")
                    return {"error": str(e)}

    def health_check(self) -> bool:
        """
        Checks if the API is healthy.

        Returns:
            bool: True if API is healthy, False otherwise.
        """
        result = self._get_with_retry("health")
        return result.get("status") == "healthy"

    def record_usage(self, customer_id: str, service: str, units: float, price: Optional[float] = None):
        """
        Sends a usage record to the internal API with retry logic.
        Skips duplicate submissions for idempotency.

        Args:
            customer_id (str): Unique customer identifier.
            service (str): Name of the service used.
            units (float): Units consumed.
            price (float, optional): Optional price. If None, API may calculate.

        Returns:
            dict: Response JSON from the API if successful or skipped status if duplicate.
        """
        key = (customer_id, service, units, price)
        if key in self._submitted_usages:
            log_info(f"Duplicate usage detected for {key}, skipping.")
            return {"status": "skipped"}

        payload = {"customer_id": customer_id, "service": service, "units": units}
        if price is not None:
            payload["price"] = price

        result = self._post_with_retry("usage", payload)
        if "error" not in result:
            self._submitted_usages.add(key)  # Mark as submitted
            result["status"] = result.get("status", "success")  # Ensure status field exists
        return result

    def get_usage(self, customer_id: str):
        """
        Retrieves usage records for a given customer from the API with retry logic.

        Args:
            customer_id (str): Unique customer identifier.

        Returns:
            dict: Response JSON containing usage data.
        """
        return self._get_with_retry(f"usage/{customer_id}")


# ----------------------------
# Example usage
# ----------------------------
if __name__ == "__main__":
    client = BillingClient(api_url="http://127.0.0.1:8000", max_retries=3, backoff_factor=2.0)

    # Health check
    print("API Healthy:", client.health_check())

    # Record usage
    result = client.record_usage(customer_id="usage_test123", service="APIRequests", units=5.5, price=1.25)
    print("Record Usage Result:", result)

    # Duplicate usage submission (should be skipped)
    duplicate = client.record_usage(customer_id="usage_test123", service="APIRequests", units=5.5, price=1.25)
    print("Duplicate Usage Result:", duplicate)

    # Retrieve usage
    usage_data = client.get_usage(customer_id="usage_test123")
    print("Retrieved Usage:", usage_data)

