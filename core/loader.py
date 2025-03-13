import pandas as pd
import os
from config.settings import DEFAULT_CSV_DELIMITER, DEFAULT_ENCODING
from utils.error_handler import ErrorHandler

class CSVLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.delimiter = DEFAULT_CSV_DELIMITER
        self.encoding = DEFAULT_ENCODING

    def load_csv(self):
        """Loads CSV content into a Pandas DataFrame."""
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File {self.file_path} not found.")
            
            df = pd.read_csv(self.file_path, delimiter=self.delimiter, encoding=self.encoding)

            if df.empty:
                raise ValueError("CSV file is empty.")

            return df  # ✅ Always return a DataFrame

        except Exception as e:
            ErrorHandler.handle_error("Failed to load CSV file.", e, critical=True)
            return None  # ✅ Return None on failure
