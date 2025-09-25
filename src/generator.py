"""
Generator module
Author: Lewis Blackwell
Description: This module reads a CSV file of customer names, assigns a unique ID to each,
and returns a list of dictionaries with 'customer_id' and 'first_name'.
It also handles logging for errors and important events.
"""

import pandas as pd
import uuid
from pathlib import Path
import logging

class Generator:
    """
    Generator class for creating customer IDs from a CSV file.
    
    Attributes:
        root_dir (Path): Root directory of the project.
        data_file (str): Relative path to the CSV file containing customer names.
        logger (logging.Logger): Logger instance for the class.
    """
    def __init__(self, root_dir: str, data_file: str = "data/Customer_Names.csv"):
        self.root_dir = Path(root_dir)
        self.data_file = data_file
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """
        Sets up a logger for the Generator class.
        Logs are written to the `logs` folder in the project root.
        """
        logger = logging.getLogger("GeneratorLogger")
        logger.setLevel(logging.DEBUG)
        
        # Ensure logs directory exists
        logs_dir = self.root_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / "generator.log"

        fh = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        if not logger.handlers:
            logger.addHandler(fh)
        return logger

    def generate_customers(self):
        """
        Reads the CSV file, generates UUIDs, and returns a list of customer dictionaries.
        Skips empty or invalid first names.
        """
        file_path = self.root_dir / self.data_file
        print(f"CSV file path: {file_path}")  # For troubleshooting

        if not file_path.exists():
            self.logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"CSV file does not exist: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            self.logger.error(f"Error reading CSV file: {e}")
            raise e

        customers = []
        for index, row in df.iterrows():
            first_name = row.get('First Name', None)
            if first_name and isinstance(first_name, str) and first_name.strip():
                customer_id = f"usage_{uuid.uuid4()}"
                customers.append({'customer_id': customer_id, 'first_name': first_name.strip()})
            else:
                self.logger.warning(f"Skipping empty/invalid row at index {index}")
        return customers

if __name__ == "__main__":
    # Test with bogus path to check logging/error handling
    print("Testing with bogus path:")
    try:
        gen = Generator(root_dir="invalid_root")
        gen.generate_customers()
    except FileNotFoundError as e:
        print(f"Caught expected error: {e}")

    # Test with correct path for local testing
    print("\nTesting with correct path:")
    root_dir_correct = Path(__file__).parent.parent  # Assuming src is one level below root
    try:
        gen = Generator(root_dir=root_dir_correct)
        customer_list = gen.generate_customers()
        print(f"Generated {len(customer_list)} customers")
        print(customer_list[:5])  # Show first 5 for sanity check
    except Exception as e:
        print(f"Unexpected error: {e}")

