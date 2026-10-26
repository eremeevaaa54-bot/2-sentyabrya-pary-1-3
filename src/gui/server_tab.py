import json
import queue
import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk
from ..server.http_server import HttpServer


class ServerTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._queue: "queue.Queue[str]" = queue.Queue()
        self._server = None
        self._build_ui()
        self.after(100, self._poll_queue)

    def _build_ui(self):
        tk.Label(self, text="Порт:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.port_var = tk.StringVar(value="8080")
        tk.Entry(self, textvariable=self.port_var, width=10).grid(row=0, column=1, sticky="w", padx=4)

        tk.Button(self, text="Запустить", command=self.start_server,
                  bg="#4CAF50", fg="white").grid(row=0, column=2, padx=4)
        tk.Button(self, text="Остановить", command=self.stop_server,
                  bg="#F44336", fg="white").grid(row=0, column=3, padx=4)

        self.indicator = tk.Label(self, text="⚫", fg="gray", font=("Arial", 18))
        self.indicator.grid(row=0, column=4, padx=8)

        tk.Button(self, text="Очистить лог", command=self.clear_log).grid(
            row=0, column=5, padx=4)
        tk.Button(self, text="Открыть в браузере",
                  command=lambda: webbrowser.open("http://localhost:8080/")).grid(
            row=0, column=6, padx=4)

        self.log_text = tk.Text(self, height=22, width=110, state="disabled")
        self.log_text.grid(row=1, column=0, columnspan=7, sticky="nsew", padx=4, pady=4)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def start_server(self):
        if self._server:
            return
        try:
            port = int(self.port_var.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный порт")
            return
        try:
            self._server = HttpServer(port=port, log_callback=self._queue.put)
            self._server.start()
        except OSError as exc:
            messagebox.showerror("Ошибка", f"Не удалось запустить: {exc}")
            self._server = None
            return
        self.indicator.configure(text="🟢", fg="green")
        self._append(f"[{port}] Сервер запущен")

    def stop_server(self):
        if not self._server:
            return
        self._server.stop()
        self._server = None
        self.indicator.configure(text="⚫", fg="gray")
        self._append("Сервер остановлен")

    def clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _append(self, text: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _poll_queue(self):
        try:
            while True:
                raw = self._queue.get_nowait()
                try:
                    # Пытаемся превратить строку JSON в объект Python
                    record = json.loads(raw)
                    line = (f"{record.get('time', '')}  |  "
                            f"{record.get('method', ''):6}  |  "
                            f"{record.get('path', ''):25}  |  "
                            f"{record.get('status', '')}  |  "
                            f"{record.get('length', '')} b")
                except Exception:
                    # Если JSON битый или там русские буквы, выводим как есть
                    line = f"RAW: {raw}"

                self._append(line)
        except queue.Empty:
            pass

        # Планируем следующую проверку через 100 мс
        self.after(100, self._poll_queue)