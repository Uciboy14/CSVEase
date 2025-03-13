import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
from core.loader import CSVLoader
from core.processor import CSVProcessor
from core.exporter import CSVExporter

class CSVEaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSVEase - CSV Processor")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Initialize variables
        self.file_path = None
        self.data = None
        self.processor = None

        # Create UI components
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open CSV", command=self.load_csv)
        file_menu.add_command(label="Save CSV", command=self.save_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Uppercase Headers", command=self.apply_uppercase_headers)
        edit_menu.add_command(label="Replace Value", command=self.replace_value_popup)
        edit_menu.add_command(label="Sort by Column", command=self.sort_popup)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def create_widgets(self):
        """Create UI components."""
        # File Selection Button
        self.file_btn = tk.Button(self.root, text="Open CSV", command=self.load_csv, bg="#007BFF", fg="white", font=("Arial", 12))
        self.file_btn.pack(pady=10)

        # Treeview for displaying CSV
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        # Action Buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(fill="x", pady=5)

        self.process_btn = tk.Button(button_frame, text="Apply Changes", command=self.process_data, bg="#FFA500", fg="white", font=("Arial", 12))
        self.process_btn.pack(side="left", padx=10)

        self.export_btn = tk.Button(button_frame, text="Export CSV", command=self.save_csv, bg="#28A745", fg="white", font=("Arial", 12))
        self.export_btn.pack(side="left", padx=10)

        self.reset_btn = tk.Button(button_frame, text="Reset", command=self.reset_table, bg="#DC3545", fg="white", font=("Arial", 12))
        self.reset_btn.pack(side="left", padx=10)

        # Status Bar
        self.status_label = tk.Label(self.root, text="Welcome to CSVEase!", bd=1, relief=tk.SUNKEN, anchor="w", bg="#D1ECF1", fg="#0C5460")
        self.status_label.pack(fill="x", padx=10, pady=5)

    def load_csv(self):
        """Load a CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        self.file_path = file_path
        loader = CSVLoader(file_path)
        self.data = loader.load_csv()

        if self.data is not None and not self.data.empty:
            self.processor = CSVProcessor(self.data)
            self.display_data()
            self.status_label.config(text="✅ File loaded successfully!")
        else:
            messagebox.showerror("Error", "Failed to load CSV.")

    def display_data(self):
        """Display CSV data in the table."""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"

        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def apply_uppercase_headers(self):
        """Convert headers to uppercase."""
        if self.processor:
            self.processor.uppercase_headers()
            self.display_data()
            self.status_label.config(text="🔠 Headers converted to uppercase!")

    def replace_value_popup(self):
        """Popup to replace values."""
        popup = tk.Toplevel(self.root)
        popup.title("Replace Value")
        popup.geometry("300x150")

        tk.Label(popup, text="Find:").pack(pady=5)
        find_entry = tk.Entry(popup)
        find_entry.pack(pady=5)

        tk.Label(popup, text="Replace with:").pack(pady=5)
        replace_entry = tk.Entry(popup)
        replace_entry.pack(pady=5)

        def replace():
            if self.processor:
                self.processor.replace_value(find_entry.get(), replace_entry.get())
                self.display_data()
                self.status_label.config(text="🔄 Values replaced successfully!")
                popup.destroy()

        tk.Button(popup, text="Apply", command=replace).pack(pady=10)

    def sort_popup(self):
        """Popup to sort by column."""
        popup = tk.Toplevel(self.root)
        popup.title("Sort Data")
        popup.geometry("300x150")

        tk.Label(popup, text="Sort by Column:").pack(pady=5)
        column_entry = tk.Entry(popup)
        column_entry.pack(pady=5)

        def sort_data():
            if self.processor:
                col_name = column_entry.get()
                if col_name in self.data.columns:
                    self.processor.sort_by_column(col_name, ascending=True)
                    self.display_data()
                    self.status_label.config(text=f"📊 Sorted by {col_name}!")
                else:
                    messagebox.showerror("Error", "Column not found!")
                popup.destroy()

        tk.Button(popup, text="Sort", command=sort_data).pack(pady=10)

    def process_data(self):
        """Apply all processing changes."""
        if self.processor:
            self.processor.remove_duplicates()
            self.display_data()
            self.status_label.config(text="✅ Processing applied!")

    def save_csv(self):
        """Save processed CSV file."""
        if self.processor:
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if save_path:
                exporter = CSVExporter(save_path, self.processor.get_dataframe())
                exporter.save_csv()
                self.status_label.config(text="📁 File saved successfully!")

    def reset_table(self):
        """Reset table to original CSV."""
        if self.file_path:
            self.load_csv()
            self.status_label.config(text="🔄 Data reset!")

    def show_about(self):
        """Show About message."""
        messagebox.showinfo("About CSVEase", "CSVEase v1.0\nA simple CSV processing tool.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEaseApp(root)
    root.mainloop()
