import tkinter as tk
from tkinter import ttk

class HeaderTable(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._build()
        self.add_row("User-Agent", "HttpGui/1.0")
        self.add_row("Accept", "*/*")

    def _build(self):
        self.tree = ttk.Treeview(self, columns=("name", "value"), show="headings", height=4)
        self.tree.heading("name", text="Заголовок")
        self.tree.heading("value", text="Значение")
        self.tree.column("name", width=180)
        self.tree.column("value", width=380)
        self.tree.grid(row=0, column=0, columnspan=3, sticky="we")

        tk.Label(self, text="Имя:").grid(row=1, column=0, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var, width=22).grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Значение:").grid(row=2, column=0, sticky="w")
        self.value_var = tk.StringVar()
        tk.Entry(self, textvariable=self.value_var, width=50).grid(row=2, column=1, sticky="we")

        tk.Button(self, text="Добавить", command=self._add_from_fields).grid(row=1, column=2, padx=4)
        tk.Button(self, text="Удалить", command=self._remove_selected).grid(row=2, column=2, padx=4)
        self.columnconfigure(1, weight=1)

    def add_row(self, name: str, value: str) -> None:
        self.tree.insert("", "end", values=(name, value))

    def _add_from_fields(self):
        name = self.name_var.get().strip()
        value = self.value_var.get().strip()
        if name:
            self.add_row(name, value)
            self.name_var.set("")
            self.value_var.set("")

    def _remove_selected(self):
        for item in self.tree.selection():
            self.tree.delete(item)

    def get_headers(self) -> dict:
        headers = {}
        for item in self.tree.get_children():
            name, value = self.tree.item(item, "values")
            if name: headers[name] = value
        return headers