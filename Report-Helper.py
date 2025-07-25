import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox

class CVASearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CVA Finder")
        self.root.geometry("1200x700")
        self.filename = "cva_findings.csv"
        self.data = []
        self.load_data_from_file()

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(root, textvariable=self.search_var, width=60)
        search_entry.pack(pady=10)
        search_entry.bind("<KeyRelease>", self.search)

        self.tree = ttk.Treeview(root, columns=("CVA ID", "Title"), show="headings", height=25)
        self.tree.heading("CVA ID", text="CVA ID")
        self.tree.heading("Title", text="Title")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.show_details)

        add_button = tk.Button(root, text="Add New Finding", command=self.open_add_finding_dialog)
        add_button.pack(pady=10)

        self.load_data(self.data)

    def load_data_from_file(self):
        try:
            with open(self.filename, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                self.data = [row for row in reader]
        except FileNotFoundError:
            self.data = []

    def save_to_csv(self):
        fieldnames = ["CVA ID", "Title", "Description", "Steps To Reproduce", "Risk Rating Note", "CVSS", "Reference SOWs", "Recommendation"]
        with open(self.filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data:
                clean_row = {key: row.get(key, "") for key in fieldnames}
                writer.writerow(clean_row)

    def load_data(self, data):
        self.tree.delete(*self.tree.get_children())
        for row in data:
            self.tree.insert("", "end", values=(row.get("CVA ID", ""), row.get("Title", "")))

    def search(self, event=None):
        keyword = self.search_var.get().lower()
        filtered = [row for row in self.data if keyword in row.get("CVA ID", "").lower() or keyword in row.get("Title", "").lower()]
        self.load_data(filtered)

    def show_details(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        values = self.tree.item(selected_item)["values"]
        cva_id, title = values[0], values[1]
        finding = next((f for f in self.data if f["CVA ID"] == cva_id and f["Title"] == title), None)

        if not finding:
            return

        detail_window = tk.Toplevel()
        detail_window.title(f"Details - {title}")
        detail_window.geometry("700x700")

        sections = ["CVA ID", "Title", "Description", "Steps To Reproduce", "Risk Rating Note", "CVSS", "Reference SOWs", "Recommendation"]

        for i, section in enumerate(sections):
            content = finding.get(section, "")
            label = tk.Label(detail_window, text=f"{section}:", anchor='w', justify='left', font=("Arial", 10, "bold"))
            label.grid(row=i, column=0, sticky="nw", padx=10, pady=4)

            text_widget = tk.Text(detail_window, height=3, width=80, wrap="word")
            text_widget.insert("1.0", content)
            text_widget.config(state="disabled")
            text_widget.grid(row=i, column=1, padx=5, pady=4)

            # Copy button for section
            def copy_section(c=content):
                self.root.clipboard_clear()
                self.root.clipboard_append(c)

            copy_btn = tk.Button(detail_window, text="Copy", command=copy_section)
            copy_btn.grid(row=i, column=2, padx=5)

    def open_add_finding_dialog(self):
        dialog = tk.Toplevel()
        dialog.title("Add New Finding")
        dialog.geometry("600x500")

        fields = ["CVA ID", "Title", "Description", "Steps To Reproduce", "Risk Rating Note", "CVSS", "Reference SOWs", "Recommendation"]
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CVASearchApp(root)
    root.mainloop()
