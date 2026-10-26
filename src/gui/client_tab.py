import json
import queue
import threading
import tkinter as tk
from tkinter import ttk
from ..client.http_client import HttpClient, HttpError
from ..net.tcp_client import ConnectionError_, TimeoutError_
from .widgets import HeaderTable

class ClientTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._queue: "queue.Queue[dict]" = queue.Queue()
        self._build_ui()
        self.after(100, self._poll_queue)

    def _build_ui(self):
        tk.Label(self, text="URL:").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.url_var = tk.StringVar(value="http://example.com/")
        tk.Entry(self, textvariable=self.url_var, width=80).grid(
            row=0, column=1, columnspan=3, sticky="we", padx=4, pady=4)

        tk.Label(self, text="Метод:").grid(row=1, column=0, sticky="w", padx=4)
        self.method_var = tk.StringVar(value="GET")
        ttk.Combobox(self, textvariable=self.method_var, values=["GET", "POST"],
                     state="readonly", width=10).grid(row=1, column=1, sticky="w", padx=4)

        tk.Label(self, text="Заголовки:").grid(row=2, column=0, sticky="nw", padx=4)
        self.header_table = HeaderTable(self)
        self.header_table.grid(row=2, column=1, columnspan=3, sticky="we", padx=4, pady=4)

        tk.Label(self, text="Тело (POST):").grid(row=3, column=0, sticky="nw", padx=4)
        self.body_text = tk.Text(self, height=5, width=80)
        self.body_text.grid(row=3, column=1, columnspan=3, sticky="we", padx=4, pady=4)

        tk.Button(self, text="Отправить", command=self.send_request,
                  bg="#4CAF50", fg="white").grid(row=4, column=1, sticky="w", padx=4)
        tk.Button(self, text="Очистить", command=self.clear).grid(
            row=4, column=2, sticky="w", padx=4)
        self.spinner = tk.Label(self, text="")
        self.spinner.grid(row=4, column=3, sticky="w")

        tk.Label(self, text="Ответ:").grid(row=5, column=0, sticky="nw", padx=4)
        self.response_text = tk.Text(self, height=20, width=100, state="disabled")
        self.response_text.grid(row=5, column=1, columnspan=3, sticky="nsew", padx=4, pady=4)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)

    def clear(self):
        self.body_text.delete("1.0", "end")
        self._set_response("")

    def _set_response(self, text: str):
        self.response_text.configure(state="normal")
        self.response_text.delete("1.0", "end")
        self.response_text.insert("1.0", text)
        self.response_text.configure(state="disabled")

    def send_request(self):
        url = self.url_var.get().strip()
        method = self.method_var.get()
        body = self.body_text.get("1.0", "end").rstrip("\n").encode()
        headers = self.header_table.get_headers()
        self.spinner.configure(text="Отправка...")
        threading.Thread(target=self._worker, args=(method, url, body, headers),
                         daemon=True).start()

    def _worker(self, method, url, body, headers):
        try:
            client = HttpClient(timeout=5.0)
            if method == "GET":
                resp = client.get(url, headers=headers)
            else:
                resp = client.post(url, body, content_type="text/plain", headers=headers)
            result = {
                "ok": True, "status": resp.status, "reason": resp.reason,
                "headers": dict(resp.headers),
                "body": resp.body.decode("utf-8", errors="replace"),
            }
        except (ConnectionError_, TimeoutError_, HttpError) as exc:
            result = {"ok": False, "error": str(exc)}
        except Exception as exc:
            result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        self._queue.put(result)

    def _poll_queue(self):
        try:
            while True:
                item = self._queue.get_nowait()
                self._render(item)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _render(self, item: dict):
        self.spinner.configure(text="")
        if not item.get("ok"):
            self._set_response(f"ОШИБКА: {item['error']}")
            return
        lines = [f"Статус: {item['status']} {item['reason']}", "", "Заголовки:"]
        for key, value in item["headers"].items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        lines.append("Тело:")
        body = item["body"]
        try:
            body = json.dumps(json.loads(body), indent=2, ensure_ascii=False)
        except Exception:
            pass
        lines.append(body)
        self._set_response("\n".join(lines))