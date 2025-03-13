import unittest
import pandas as pd
from core.loader import CSVLoader

class TestCSVLoader(unittest.TestCase):
    def setUp(self):
        """Set up a sample CSV file for testing"""
        self.test_file = "test_data.csv"
        with open(self.test_file, "w") as f:
            f.write("Name,Age,City\nAlice,25,New York\nBob,30,London")

    def tearDown(self):
        """Clean up after tests"""
        import os
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_csv(self):
        """Test if CSVLoader loads a CSV file correctly"""
        loader = CSVLoader(self.test_file)
        df = loader.load_csv()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (2, 3))  # 2 rows, 3 columns
        self.assertListEqual(list(df.columns), ["Name", "Age", "City"])

if __name__ == "__main__":
    unittest.main()
