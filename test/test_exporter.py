import unittest
import os
import pandas as pd
from core.exporter import CSVExporter

class TestCSVExporter(unittest.TestCase):
    def setUp(self):
        """Create sample data for testing"""
        self.file_path = "test_output.csv"
        data = {"Name": ["Alice", "Bob"], "Age": [25, 30], "City": ["NY", "London"]}
        self.df = pd.DataFrame(data)

    def tearDown(self):
        """Clean up test files"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_save_csv(self):
        """Test if CSV file is saved correctly"""
        exporter = CSVExporter(self.file_path, self.df)
        exporter.save_csv()
        self.assertTrue(os.path.exists(self.file_path))

        # Verify file contents
        loaded_df = pd.read_csv(self.file_path)
        self.assertEqual(loaded_df.shape, self.df.shape)
        self.assertListEqual(list(loaded_df.columns), list(self.df.columns))

if __name__ == "__main__":
    unittest.main()
