import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess, json, os

class ExifToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ExifTool GUI")
        self.selected_files = []
        self.metadata_entries = {}  # maps metadata tag -> Entry widget
        self.metadata = {}  # holds the metadata loaded from the first file

        self.create_widgets()

    def create_widgets(self):
        # --- File Selection Frame ---
        file_frame = ttk.LabelFrame(self.root, text="Select Files")
        file_frame.pack(fill="x", padx=10, pady=5)

        select_button = ttk.Button(file_frame, text="Browse Files", command=self.browse_files)
        select_button.pack(side="left", padx=5, pady=5)

        self.file_listbox = tk.Listbox(file_frame, height=5)
        self.file_listbox.pack(fill="both", padx=5, pady=5)

        # --- Metadata Preview & Edit Frame ---
        meta_frame = ttk.LabelFrame(self.root, text="Metadata Preview & Edit")
        meta_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Create a canvas with scrollbar for the metadata form
        self.meta_canvas = tk.Canvas(meta_frame)
        self.meta_scrollbar = ttk.Scrollbar(meta_frame, orient="vertical", command=self.meta_canvas.yview)
        self.meta_inner_frame = ttk.Frame(self.meta_canvas)

        self.meta_inner_frame.bind(
            "<Configure>",
            lambda e: self.meta_canvas.configure(scrollregion=self.meta_canvas.bbox("all"))
        )

        self.meta_canvas.create_window((0, 0), window=self.meta_inner_frame, anchor="nw")
        self.meta_canvas.configure(yscrollcommand=self.meta_scrollbar.set)

        self.meta_canvas.pack(side="left", fill="both", expand=True)
        self.meta_scrollbar.pack(side="right", fill="y")

        # --- ExifTool Options Frame ---
        options_frame = ttk.LabelFrame(self.root, text="ExifTool Options")
        options_frame.pack(fill="x", padx=10, pady=5)

        self.overwrite_var = tk.BooleanVar()
        overwrite_cb = ttk.Checkbutton(options_frame, text="Overwrite Original Files", variable=self.overwrite_var)
        overwrite_cb.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        ttk.Label(options_frame, text="Custom Options:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.custom_options_entry = ttk.Entry(options_frame)
        self.custom_options_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        options_frame.columnconfigure(1, weight=1)

        # --- Output Folder Frame ---
        output_frame = ttk.LabelFrame(self.root, text="Output Folder (Optional)")
        output_frame.pack(fill="x", padx=10, pady=5)

        self.use_output_var = tk.BooleanVar()
        use_output_cb = ttk.Checkbutton(output_frame, text="Save to new folder", variable=self.use_output_var, command=self.toggle_output_entry)
        use_output_cb.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.output_entry = ttk.Entry(output_frame, state="disabled")
        self.output_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        output_browse = ttk.Button(output_frame, text="Browse", command=self.browse_output_folder, state="disabled")
        output_browse.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.output_browse_button = output_browse
        output_frame.columnconfigure(1, weight=1)

        # --- Apply Changes Button ---
        apply_button = ttk.Button(self.root, text="Apply Changes", command=self.apply_changes)
        apply_button.pack(padx=10, pady=10)

    def toggle_output_entry(self):
        # Enable or disable the output folder entry based on the checkbox state
        if self.use_output_var.get():
            self.output_entry.config(state="normal")
            self.output_browse_button.config(state="normal")
        else:
            self.output_entry.config(state="disabled")
            self.output_browse_button.config(state="disabled")

    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)

    def browse_files(self):
        files = filedialog.askopenfilenames(title="Select Files")
        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for f in self.selected_files:
                self.file_listbox.insert(tk.END, f)
            # Load metadata for the first selected file for preview/edit
            self.load_metadata(self.selected_files[0])

    def load_metadata(self, file_path):
        # Clear any previous metadata widgets
        for widget in self.meta_inner_frame.winfo_children():
            widget.destroy()
        self.metadata_entries.clear()
        self.metadata.clear()

        try:
            # Run exiftool in JSON mode
            result = subprocess.run(["exiftool", "-json", file_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Error reading metadata:\n{result.stderr}")
                return
            data = json.loads(result.stdout)
            if data and isinstance(data, list) and len(data) > 0:
                self.metadata = data[0]
                row = 0
                # Create a row for each metadata tag (skip a few internal tags)
                for tag, value in self.metadata.items():
                    if tag in ("SourceFile", "ExifToolVersion"):
                        continue
                    ttk.Label(self.meta_inner_frame, text=tag).grid(row=row, column=0, sticky="w", padx=5, pady=2)
                    entry = ttk.Entry(self.meta_inner_frame)
                    entry.insert(0, str(value))
                    entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
                    self.metadata_entries[tag] = entry
                    row += 1
                self.meta_inner_frame.columnconfigure(1, weight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

    def apply_changes(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return

        # Build the exiftool command line
        cmd = ["exiftool"]

        # Add the overwrite option if selected
        if self.overwrite_var.get():
            cmd.append("-overwrite_original")

        # Add any custom options (split by space)
        custom_options = self.custom_options_entry.get().strip()
        if custom_options:
            cmd.extend(custom_options.split())

        # Compare each edited metadata value to the original
        for tag, entry in self.metadata_entries.items():
            new_value = entry.get().strip()
            if new_value != str(self.metadata.get(tag, "")):
                # Format the change as -TAG=VALUE
                cmd.append(f"-{tag}={new_value}")

        # Specify the output folder if the option is enabled
        if self.use_output_var.get():
            output_folder = self.output_entry.get().strip()
            if output_folder:
                # exiftool -o uses the output directory while preserving file names
                cmd.extend(["-o", output_folder])

        # Append all the selected files
        cmd.extend(self.selected_files)

        # Debug: print the command to the console
        print("Running command:", " ".join(cmd))

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                messagebox.showerror("Error", f"ExifTool error:\n{result.stderr}")
            else:
                messagebox.showinfo("Success", f"Metadata updated successfully.\n{result.stdout}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExifToolGUI(root)
    root.mainloop()
