import tkinter as tk
from tkinter import ttk, messagebox
import csv
import pyperclip  # pip install pyperclip

# Load CSV data
def load_csv(filename="data.csv"):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

class CVASearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CVA Search Tool")
        self.data = load_csv()

        # Search Box
        self.search_var = tk.StringVar()
        tk.Label(root, text="Search:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(root, textvariable=self.search_var, width=50).grid(row=0, column=1, padx=5)
        tk.Button(root, text="Search", command=self.search).grid(row=0, column=2, padx=5)

        # Treeview: Show CVA ID and Title
        self.tree = ttk.Treeview(root, columns=("CVA ID", "Title"), show="headings")
        self.tree.heading("CVA ID", text="CVA ID")
        self.tree.heading("Title", text="Title")
        self.tree.column("CVA ID", width=100)
        self.tree.column("Title", width=400)
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.tree.bind("<Double-1>", self.show_details)

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.load_data(self.data)

    def load_data(self, dataset):
        self.tree.delete(*self.tree.get_children())
        for row in dataset:
            self.tree.insert("", tk.END, values=(row["CVA ID"], row["Title"]))

    def search(self):
        query = self.search_var.get().lower()
        filtered = []

        for row in self.data:
            if query in row["CVA ID"].lower() or query in row["Title"].lower():
                filtered.append(row)

        self.load_data(filtered)

    def show_details(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, "values")
        selected_cva_id = values[0]

        # Find full row
        for row in self.data:
            if row["CVA ID"] == selected_cva_id:
                self.show_popup(row)
                break

    def show_popup(self, row):
        popup = tk.Toplevel(self.root)
        popup.title(f"{row['CVA ID']} Details")
        popup.geometry("700x500")

        fields = [
            ("CVA ID", row["CVA ID"]),
            ("Title", row["Title"]),
            ("Description", row["Description"]),
            ("Risk Rating", row["Risk Rating"]),
            ("Recommended Solution", row["Recommended Solution"]),
            ("Affected Hosts", row["Affected Hosts"]),
            ("Resolved Hosts", row["Resolved Hosts"]),
        ]

        frame = tk.Frame(popup)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        for i, (label, value) in enumerate(fields):
            tk.Label(frame, text=f"{label}:", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="nw", pady=4)
            text_box = tk.Text(frame, height=3, width=60, wrap="word")
            text_box.insert("1.0", value)
            text_box.config(state="disabled")
            text_box.grid(row=i, column=1, pady=4)
            tk.Button(frame, text="Copy", command=lambda v=value: self.copy_to_clipboard(v)).grid(row=i, column=2, padx=5)

        # Copy All Button
        full_text = "\n".join([f"{label}: {value}" for label, value in fields])
        tk.Button(popup, text="Copy All", command=lambda: self.copy_to_clipboard(full_text)).pack(pady=10)

    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Text copied to clipboard.")

# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = CVASearchApp(root)
    root.mainloop()
