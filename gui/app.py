import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from core.loader import CSVLoader
from core.processor import CSVProcessor
from core.exporter import CSVExporter

class CSVEaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Processing Tool")
        self.root.geometry("900x600")
        self.root.configure(bg="#f4f4f4")

        # CSV Data
        self.df = None
        self.file_path = ""

        # Setup UI
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """Creates the menu bar."""
        menu_bar = tk.Menu(self.root)
        
        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open CSV", command=self.load_csv)
        file_menu.add_command(label="Save CSV", command=self.save_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Convert Headers to Uppercase", command=self.convert_headers)
        edit_menu.add_command(label="Remove Duplicates", command=self.remove_duplicates)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help Menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "CSV Processing Tool v1.0"))
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_widgets(self):
        """Creates the main UI components."""
        # File selection button
        self.file_label = tk.Label(self.root, text="No file selected", bg="#f4f4f4", font=("Arial", 12))
        self.file_label.pack(pady=10)

        self.select_btn = tk.Button(self.root, text="Select CSV File", command=self.load_csv, bg="#1E90FF", fg="white", font=("Arial", 12))
        self.select_btn.pack(pady=5)

        # Treeview (Table) for CSV Display
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set)
        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.config(command=self.tree.yview)

        # Processing Options
        self.options_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.options_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.options_frame, text="Find:", bg="#f4f4f4").grid(row=0, column=0)
        self.find_entry = tk.Entry(self.options_frame, width=15)
        self.find_entry.grid(row=0, column=1)

        tk.Label(self.options_frame, text="Replace with:", bg="#f4f4f4").grid(row=0, column=2)
        self.replace_entry = tk.Entry(self.options_frame, width=15)
        self.replace_entry.grid(row=0, column=3)

        self.replace_btn = tk.Button(self.options_frame, text="Replace", command=self.replace_value, bg="#FF4500", fg="white")
        self.replace_btn.grid(row=0, column=4, padx=10)

        # Sorting Dropdown
        tk.Label(self.options_frame, text="Sort by:", bg="#f4f4f4").grid(row=1, column=0)
        self.sort_column = ttk.Combobox(self.options_frame, values=[], width=15)
        self.sort_column.grid(row=1, column=1)

        self.sort_btn = tk.Button(self.options_frame, text="Sort", command=self.sort_data, bg="#008000", fg="white")
        self.sort_btn.grid(row=1, column=2, padx=10)

        # Buttons
        self.process_btn = tk.Button(self.root, text="Apply Changes", command=self.process_data, bg="#FFA500", fg="white", font=("Arial", 12))
        self.process_btn.pack(pady=5)

        self.export_btn = tk.Button(self.root, text="Export CSV", command=self.save_csv, bg="#228B22", fg="white", font=("Arial", 12))
        self.export_btn.pack(pady=5)

        # Status Bar
        self.status_label = tk.Label(self.root, text="Ready", bg="#D3D3D3", anchor="w")
        self.status_label.pack(fill="x", side="bottom")

    def load_csv(self):
        """Loads a CSV file and displays it."""
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not self.file_path:
            return

        loader = CSVLoader(self.file_path)
        self.df = loader.load_csv()

        if self.df is None or self.df.empty:
            messagebox.showerror("Error", "Failed to load CSV.")
            return

        self.file_label.config(text=self.file_path)
        self.display_csv()
        self.status_label.config(text="CSV Loaded Successfully")

    def display_csv(self):
        """Displays CSV data in the table."""
        self.tree.delete(*self.tree.get_children())

        if self.df is not None:
            self.tree["columns"] = list(self.df.columns)
            self.tree["show"] = "headings"

            for col in self.df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor="center")

            for _, row in self.df.iterrows():
                self.tree.insert("", "end", values=list(row))

            self.sort_column["values"] = list(self.df.columns)

    def convert_headers(self):
        """Converts headers to uppercase."""
        if self.df is not None:
            processor = CSVProcessor(self.df)
            processor.uppercase_headers()
            self.df = processor.get_dataframe()
            self.display_csv()
            self.status_label.config(text="Headers converted to uppercase")

    def remove_duplicates(self):
        """Removes duplicate rows."""
        if self.df is not None:
            processor = CSVProcessor(self.df)
            processor.remove_duplicates()
            self.df = processor.get_dataframe()
            self.display_csv()
            self.status_label.config(text="Duplicates removed")

    def replace_value(self):
        """Replaces values in the CSV."""
        find_text = self.find_entry.get()
        replace_text = self.replace_entry.get()

        if self.df is not None and find_text:
            processor = CSVProcessor(self.df)
            processor.replace_value(find_text, replace_text)
            self.df = processor.get_dataframe()
            self.display_csv()
            self.status_label.config(text=f"Replaced '{find_text}' with '{replace_text}'")

    def sort_data(self):
        """Sorts the data by a selected column."""
        column = self.sort_column.get()
        if column and self.df is not None:
            processor = CSVProcessor(self.df)
            processor.sort_by_column(column)
            self.df = processor.get_dataframe()
            self.display_csv()
            self.status_label.config(text=f"Sorted by '{column}'")

    def save_csv(self):
        """Exports processed CSV."""
        if self.df is not None:
            output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if output_file:
                exporter = CSVExporter(output_file, self.df)
                exporter.save_csv()
                self.status_label.config(text=f"File saved to {output_file}")

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEaseApp(root)
    root.mainloop()
