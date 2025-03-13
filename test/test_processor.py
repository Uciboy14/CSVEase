import unittest
import pandas as pd
from core.processor import CSVProcessor

class TestCSVProcessor(unittest.TestCase):
    def setUp(self):
        """Create a sample DataFrame for testing"""
        data = {"Name": ["Alice", "Bob", "Alice"], "Age": [25, 30, 25], "City": ["NY", "London", "NY"]}
        self.df = pd.DataFrame(data)
        self.processor = CSVProcessor(self.df)

    def test_uppercase_headers(self):
        """Test if headers are converted to uppercase"""
        self.processor.uppercase_headers()
        self.assertListEqual(list(self.processor.get_dataframe().columns), ["NAME", "AGE", "CITY"])

    def test_replace_value(self):
        """Test if values are replaced correctly"""
        self.processor.replace_value("Alice", "Alicia")
        self.assertIn("Alicia", self.processor.get_dataframe()["Name"].values)

    def test_add_column(self):
        """Test if a new column is added correctly"""
        self.processor.add_column("Department", "IT")
        self.assertIn("Department", self.processor.get_dataframe().columns)
        self.assertTrue((self.processor.get_dataframe()["Department"] == "IT").all())

    def test_remove_duplicates(self):
        """Test if duplicates are removed"""
        self.processor.remove_duplicates()
        self.assertEqual(len(self.processor.get_dataframe()), 2)  # 3 rows → 2 rows

    def test_sort_by_column(self):
        """Test sorting by Age"""
        self.processor.sort_by_column("Age", ascending=False)
        self.assertEqual(self.processor.get_dataframe().iloc[0]["Age"], 30)

if __name__ == "__main__":
    unittest.main()
