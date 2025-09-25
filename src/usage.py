
# src/usage.py
from crud import CRUD
from typing import Dict, List

# ----------------- Usage Factor Thresholds -----------------
# These thresholds are used to categorize customer usage.
# NOTE: These are fictional placeholder values for demonstration purposes.
#       They can be updated based on actual usage metrics in production.
LOW_THRESHOLD = 50      # usage_factor < 50 -> 'low' usage
MEDIUM_THRESHOLD = 200  # usage_factor < 200 -> 'medium' usage, >= 200 -> 'high'

class UsageAnalyzer:
    """
    UsageAnalyzer calculates usage metrics and categorizes customer usage.

    Attributes:
        crud (CRUD): Instance of the CRUD class for database interaction.
    """

    def __init__(self, crud_instance: CRUD = None):
        """
        Initialize the UsageAnalyzer.

        Args:
            crud_instance (CRUD, optional): Pass an existing CRUD instance. 
                                            If None, a new one will be created.
        """
        self.crud = crud_instance or CRUD()

    def calculate_usage_factor(self, customer_id: str) -> float:
        """
        Calculate a usage factor for a customer.
        Usage factor is defined as total units * total price / number of records.

        Args:
            customer_id (str): Customer ID to calculate usage for.

        Returns:
            float: Computed usage factor. Returns 0 if no usage records exist.
        """
        records = self.crud.read_usage_records(customer_id)
        if not records:
            return 0.0

        total_units = sum(r.get('units', 0) or 0 for r in records)
        total_price = sum(r.get('price', 0) or 0 for r in records)
        factor = (total_units * total_price) / len(records)
        return factor

    def categorize_usage(self, customer_id: str) -> str:
        """
        Categorize customer usage into 'no', 'low', 'medium', 'high'.

        Uses the thresholds defined at the top of this module.

        Args:
            customer_id (str): Customer ID to categorize.

        Returns:
            str: Usage category ('no', 'low', 'medium', 'high').
        """
        factor = self.calculate_usage_factor(customer_id)
        if factor == 0:
            return "no"
        elif factor < LOW_THRESHOLD:
            return "low"
        elif factor < MEDIUM_THRESHOLD:
            return "medium"
        else:
            return "high"

    def summarize_usage(self) -> List[Dict]:
        """
        Summarize usage for all customers.

        Returns:
            List[Dict]: List of dictionaries with customer_id, first_name, usage_factor, category.
        """
        summary = []
        all_customers = self.crud.read_all_customers()
        for customer in all_customers:
            customer_id = customer['customer_id']
            factor = self.calculate_usage_factor(customer_id)
            category = self.categorize_usage(customer_id)
            summary.append({
                "customer_id": customer_id,
                "first_name": customer['first_name'],
                "usage_factor": factor,
                "category": category
            })
        return summary

    def close(self):
        """
        Close the CRUD database connection.
        """
        self.crud.close()


# ----------------- Example Usage -----------------
if __name__ == "__main__":
    analyzer = UsageAnalyzer()

    # Example: add some usage records for testing
    analyzer.crud.create_customer("usage_test_1", "Alice")
    analyzer.crud.create_usage_record("sess_001", "usage_test_1", "ServiceA", 5, 100)
    analyzer.crud.create_usage_record("sess_002", "usage_test_1", "ServiceB", 2, 50)

    # Calculate usage factor
    factor = analyzer.calculate_usage_factor("usage_test_1")
    print(f"Usage factor for Alice: {factor}")

    # Categorize usage
    category = analyzer.categorize_usage("usage_test_1")
    print(f"Usage category for Alice: {category}")

    # Summarize all customers
    summary = analyzer.summarize_usage()
    print("All customer usage summary:")
    for record in summary:
        print(record)

    analyzer.close()
