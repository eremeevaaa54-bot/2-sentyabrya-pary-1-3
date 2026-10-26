import tkinter as tk
from tkinter import ttk
from .client_tab import ClientTab
from .server_tab import ServerTab


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HTTP-клиент и сервер — итоговый проект")
        self.geometry("1100x750")
        self.minsize(900, 600)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        self.client_tab = ClientTab(notebook)
        self.server_tab = ServerTab(notebook)

        notebook.add(self.client_tab, text="Клиент")
        notebook.add(self.server_tab, text="Сервер")

        # Корректное закрытие окна, чтобы сервер не висел в памяти
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        try:
            if hasattr(self, 'server_tab'):
                self.server_tab.stop_server()
        finally:
            self.destroy()


def run() -> None:
    app = App()
    app.mainloop()