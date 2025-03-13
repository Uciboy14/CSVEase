import pandas as pd
from utils.error_handler import ErrorHandler

class CSVProcessor:
    def __init__(self, dataframe):
        """Initialize processor with a Pandas DataFrame."""
        try:
            if dataframe is None or not isinstance(dataframe, pd.DataFrame):
                raise ValueError("Invalid Data: Expected a Pandas DataFrame.")
            if dataframe.empty:
                raise ValueError("CSV file is empty.")
            self.df = dataframe
        except Exception as e:
            ErrorHandler.handle_error("Failed to initialize CSVProcessor.", e, critical=True)

    def uppercase_headers(self):
        """Convert all headers to uppercase."""
        try:
            self.df.columns = self.df.columns.str.upper()
        except Exception as e:
            ErrorHandler.handle_error("Error converting headers to uppercase.", e)

    def replace_value(self, old_value, new_value):
        """Replace occurrences of old_value with new_value in all rows."""
        try:
            self.df = self.df.replace(old_value, new_value)
        except Exception as e:
            ErrorHandler.handle_error("Error replacing values in CSV.", e)
            
    def add_column(self, column_name, default_value=""):
        """Add a new column with a default value."""
        try:
            self.df[column_name] = default_value
        except Exception as e:
            ErrorHandler.handle_error("Error adding new column.", e)

    def remove_duplicates(self):
        """Remove duplicate rows."""
        try:
            self.df = self.df.drop_duplicates()
        except Exception as e:
            ErrorHandler.handle_error("Error removing duplicates.", e)

    def filter_rows(self, column_name, condition):
        """Filter rows based on a condition."""
        try:
            self.df = self.df[self.df[column_name].apply(condition)]
        except Exception as e:
            ErrorHandler.handle_error("Error filtering rows.", e)

    def sort_by_column(self, column_name, ascending=True):
        """Sort data by a specific column."""
        try:
            self.df = self.df.sort_values(by=column_name, ascending=ascending)
        except Exception as e:
            ErrorHandler.handle_error("Error sorting data.", e)

    def get_dataframe(self):
        """Return the processed DataFrame."""
        return self.df
