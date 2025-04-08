from copy import copy
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from openpyxl.styles import Font
import pandas as pd

from exception_catcher import exception_catcher
from settings import Settings  # Assuming Settings is in a separate file


class DirectoryIndexUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory Indexer")
        self.root.geometry("600x250")
        self.root.resizable(False, False)

        self.settings = Settings()  # Initialize with defaults

        # Use a frame for centering
        frame = tk.Frame(root)
        frame.pack(expand=True)

        # Input Directory
        tk.Label(frame, text="Input Directory:").pack(anchor="w", padx=10, pady=(10, 2))
        self.in_directory_var = tk.StringVar(value=self.settings.in_directory)
        self.in_directory_entry = tk.Entry(frame, textvariable=self.in_directory_var, width=60)
        self.in_directory_entry.pack(padx=10)
        tk.Button(frame, text="Browse", command=self.select_in_directory).pack(pady=2)

        # File Extensions
        tk.Label(frame, text="File Extensions (List separated by commas, e.g: txt. xls, xlsx):").pack(anchor="w", padx=10, pady=(10, 2))
        self.extensions_var = tk.StringVar(value=self.settings.extensions)
        self.extensions_entry = tk.Entry(frame, textvariable=self.extensions_var, width=60)
        self.extensions_entry.pack(padx=10)

        # Output Path
        tk.Label(frame, text="Output Directory:").pack(anchor="w", padx=10, pady=(10, 2))
        self.out_path_var = tk.StringVar(value=self.settings.out_path)
        self.out_path_entry = tk.Entry(frame, textvariable=self.out_path_var, width=60)
        self.out_path_entry.pack(padx=10)
        tk.Button(frame, text="Browse", command=self.select_out_directory).pack(pady=2)

        # Index Directory Button
        tk.Button(frame, text="Index Directory", command=self.index_directory).pack(padx=10, pady=2)

    def select_in_directory(self):
        """Open file dialog to select input directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.in_directory_var.set(directory)

    def select_out_directory(self):
        """Open file dialog to select output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.out_path_var.set(directory)

    @exception_catcher
    def index_directory(self):
        """Indexes the directory and saves the result as an Excel file."""
        
        # Retrieve and validate settings
        self.settings.in_directory = os.path.abspath(self.in_directory_var.get())
        self.settings.extensions = self.extensions_var.get()
        self.settings.out_path = os.path.abspath(self.out_path_var.get())
        self.settings.validate()

        # Parse extensions
        allowed_extensions = set(self.settings.extensions.replace(" ", "").split(",")) if self.settings.extensions != ".*" else None

        data = []  # List to store directory index data
        files_count = 0
        folders_count = 0

        def traverse_directory(directory: str, level: int):
            """Recursively traverses the directory while maintaining order."""
            nonlocal files_count, folders_count
            # Add the current folder
            data.append([os.path.basename(directory), directory, level, "Folder"])
            folders_count += 1

            # Get directory contents
            try:
                entries = sorted(os.listdir(directory), key=lambda x: (os.path.isfile(os.path.join(directory, x)), x.lower()))
            except PermissionError:
                return  # Skip directories that cannot be accessed

            # Process files first
            for entry in entries:
                full_path = os.path.join(directory, entry)
                if os.path.isfile(full_path):
                    # Filter by extensions
                    if allowed_extensions is None or any(full_path.lower().endswith(ext.lower()) for ext in allowed_extensions):
                        data.append([entry, full_path, level + 1, "File"])
                        files_count += 1

            # Process subfolders
            for entry in entries:
                full_path = os.path.join(directory, entry)
                if os.path.isdir(full_path):
                    traverse_directory(full_path, level + 1)

        # Start traversal from root
        traverse_directory(self.settings.in_directory, 0)

        # Convert to DataFrame and save to Excel
        df = pd.DataFrame(data, columns=["Name", "Path", "Sub-folder Level", "Type"])
        
        # Now prepare the second sheet (Settings info)
        settings_data = [
            ["Input Directory", self.settings.in_directory],
            ["File Extensions", self.settings.extensions],
            ["Output Directory", self.settings.out_path],
            ["Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ["Files Count", files_count],
            ["Folders Count", folders_count],
            ["Total Entries", files_count + folders_count]
        ]
        
        settings_df = pd.DataFrame(settings_data, columns=["Setting Name", "Value"])

        # Excel writer to handle multiple sheets (use openpyxl engine)
        output_file = os.path.join(self.settings.out_path, "directory_index.xlsx")

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            # Write the first sheet (index of files/folders)
            df.to_excel(writer, sheet_name="Index", index=False)

            # Write the second sheet (settings)
            settings_df.to_excel(writer, sheet_name="Infos", index=False, header=False)

            # Formatting for Index sheet
            index_sheet = writer.sheets["Index"]
            index_sheet.column_dimensions["A"].width = 30  # Adjust column width for Name
            index_sheet.column_dimensions["B"].width = 50  # Adjust column width for Path
            index_sheet.column_dimensions["C"].width = 20  # Adjust column width for Sub-folder Level
            index_sheet.column_dimensions["D"].width = 15  # Adjust column width for Type

            # Formatting for Settings sheet
            info_sheet = writer.sheets["Infos"]
            info_sheet.column_dimensions["A"].width = 25  # Adjust column width for Setting Name
            info_sheet.column_dimensions["B"].width = 40  # Adjust column width for Value

            # Index
            for cell in index_sheet[1]:  # First row
                cell.font = Font(bold=True)
            for cell in range(1, len(index_sheet["B"])):  # Path column
                new_style = copy(index_sheet["B"][cell].alignment)
                new_style.horizontal = 'right'
                index_sheet["B"][cell].alignment = new_style

            # Infos
            for cell in range(len(info_sheet["A"])):  # First columun
                info_sheet["A"][cell].font = Font(bold=True)

            # === Apply Filtering & Sorting ===
            index_sheet.auto_filter.ref = index_sheet.dimensions  # Enable filter on all data

            # === Freeze the header row ===
            index_sheet.freeze_panes = "A2"  # Freeze the first row (header)

        # Show success notification
        messagebox.showinfo("Success", f"Indexing complete.\nFile saved to: {output_file}")
        print(f"Indexing complete. File saved to: {output_file}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DirectoryIndexUI(root)
    root.mainloop()
