from core.loader import CSVLoader
from core.processor import CSVProcessor

csv_file = "data/test_csv.csv"  # ✅ Correct file path

# Load CSV as a DataFrame
loader = CSVLoader(csv_file)
data = loader.load_csv()

# ✅ Properly check if data is valid
if data is not None and not data.empty:
    processor = CSVProcessor(data)
    if processor.df is not None:
        print("✅ Data successfully loaded and processed.")
        print(processor.get_dataframe().to_string(index=False))  # ✅ Print all rows without index
else:
    print("❌ No valid data to process.")
