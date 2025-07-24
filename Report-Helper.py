import tkinter as tk
from tkinter import ttk
import csv

class CVASearchApp:
    def __init__(self, root):
        self.filename = 'finding.csv'
        self.data = self.load_csv()
        self.create_ui(root)

    def load_csv(self):
        try:
            with open(self.filename, newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            return []

    def create_ui(self, root):
        root.title("CVA Finder")
        root.geometry("600x400")

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(root, textvariable=self.search_var, width=50)
        search_entry.pack(pady=10)
        search_entry.bind("<KeyRelease>", self.perform_search)

        self.tree = ttk.Treeview(root, columns=("CVA ID", "Title"), show="headings")
        self.tree.heading("CVA ID", text="CVA ID")
        self.tree.heading("Title", text="Title")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.show_details)

        add_button = tk.Button(root, text="Add New Finding", command=self.open_add_finding_dialog)
        add_button.pack(pady=10)

        self.load_data(self.data)

    def load_data(self, dataset):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in dataset:
            self.tree.insert("", "end", values=(item["CVA ID"], item["Title"]))

    def perform_search(self, event=None):
        query = self.search_var.get().lower()
        filtered = [row for row in self.data if query in row["CVA ID"].lower() or query in row["Title"].lower()]
        self.load_data(filtered)

    def show_details(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected, "values")
        cva_id = values[0]

        finding = next((row for row in self.data if row["CVA ID"] == cva_id), None)
        if finding:
            self.show_finding_popup(finding)

    def show_finding_popup(self, finding):
        popup = tk.Toplevel()
        popup.title(f"Finding: {finding['CVA ID']}")
        popup.geometry("600x400")

        text = tk.Text(popup, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)

        content = ""
        for key, value in finding.items():
            content += f"{key}:\n{value}\n\n"

        text.insert("1.0", content)
        text.config(state="disabled")

        def copy_to_clipboard():
            popup.clipboard_clear()
            popup.clipboard_append(content)
            popup.update()

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Copy to Clipboard", command=copy_to_clipboard).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Close", command=popup.destroy).pack(side="left", padx=10)

    def open_add_finding_dialog(self):
        dialog = tk.Toplevel()
        dialog.title("Add New Finding")

        fields = ["CVA ID", "Title", "Description", "Steps To Reproduce", "Risk Rating Note", "CVSS", "Reference SOWs"]
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(dialog, text=field).grid(row=i, column=0, sticky="w", padx=10, pady=2)
            entry = tk.Entry(dialog, width=60)
            entry.grid(row=i, column=1, padx=10, pady=2)
            entries[field] = entry

        def save_entry():
            new_data = {field: entries[field].get() for field in fields}
            self.data.append(new_data)
            self.save_to_csv()
            self.load_data(self.data)
            dialog.destroy()

        tk.Button(dialog, text="Save", command=save_entry).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def save_to_csv(self):
        fieldnames = ["CVA ID", "Title", "Description", "Steps To Reproduce", "Risk Rating Note", "CVSS", "Reference SOWs"]
        with open(self.filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

if __name__ == "__main__":
    root = tk.Tk()
    app = CVASearchApp(root)
    root.mainloop()
