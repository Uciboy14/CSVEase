import pandas as pd
from core.processor import CSVProcessor
from core.loader import CSVLoader
from core.exporter import CSVExporter  # Importing the exporter module

# Load CSV as DataFrame
csv_file = "data/test_csv.csv"
output_file = "data/processed_test_data.csv"

loader = CSVLoader(csv_file)
data = loader.load_csv()

# Process the DataFrame
if data is not None and not data.empty:
    processor = CSVProcessor(data)
    processor.uppercase_headers()
    processor.replace_value("Alice", "Alicia")
    processor.add_column("Department", "IT")
    processor.remove_duplicates()
    processor.sort_by_column("Age", ascending=True)

    processed_data = processor.get_dataframe()

    # Use Exporter to save the processed data
    exporter = CSVExporter(output_file, processed_data)
    exporter.save_csv()

    print(f"✅ Processed data saved to {output_file}")
    print(processed_data.head())  # Preview processed data
else:
    print("❌ No valid data to process.")
