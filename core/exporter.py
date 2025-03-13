# core/exporter.py

import csv
from config.settings import DEFAULT_CSV_DELIMITER, DEFAULT_ENCODING

class CSVExporter:
    def __init__(self, file_path, data):
        """Initialize exporter with a file path and data."""
        self.file_path = file_path
        self.data = data
        self.delimiter = DEFAULT_CSV_DELIMITER
        self.encoding = DEFAULT_ENCODING

    def save_csv(self):
        """Save the processed CSV data to a file."""
        try:
            with open(self.file_path, mode='w', encoding=self.encoding, newline='') as file:
                writer = csv.writer(file, delimiter=self.delimiter)
                writer.writerows(self.data)
            print(f"File saved successfully at {self.file_path}")
        except Exception as e:
            print(f"Error saving CSV file: {e}")
