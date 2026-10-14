import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import socket
import subprocess
import platform
import sqlite3
import json
import threading
import queue
from datetime import datetime
import time


DB_FILE = "scanner.db"

# پورت‌های رایج برای اسکن
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}


# ============================================================
# دیتابیس
# ============================================================
class ScanDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT,
                ip TEXT,
                scan_time TEXT,
                open_ports INTEGER,
                total_ports INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                port INTEGER,
                service TEXT,
                status TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(id)
            )
        """)
        self.conn.commit()

    def create_scan(self, host, ip, total):
        self.cursor.execute("""
            INSERT INTO scans (host, ip, scan_time, open_ports, total_ports)
            VALUES (?, ?, ?, ?, ?)
        """, (host, ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, total))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_port(self, scan_id, port, service, status):
        self.cursor.execute("""
            INSERT INTO ports (scan_id, port, service, status)
            VALUES (?, ?, ?, ?)
        """, (scan_id, port, service, status))
        self.conn.commit()

    def update_scan_count(self, scan_id, open_count):
        self.cursor.execute("""
            UPDATE scans SET open_ports = ? WHERE id = ?
        """, (open_count, scan_id))
        self.conn.commit()

    def get_history(self, limit=20):
        self.cursor.execute("""
            SELECT id, host, ip, scan_time, open_ports, total_ports
            FROM scans ORDER BY id DESC LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def get_scan_details(self, scan_id):
        self.cursor.execute("""
            SELECT port, service, status FROM ports WHERE scan_id = ?
        """, (scan_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()


# ============================================================
# اسکنر شبکه
# ============================================================
class NetworkScanner:
    @staticmethod
    def resolve_host(host):
        """تبدیل دامنه به IP"""
        try:
            return socket.gethostbyname(host)
        except socket.gaierror:
            return None

    @staticmethod
    def ping(host, timeout=2):
        """پینگ گرفتن"""
        param = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            result = subprocess.run(
                ["ping", param, "1", "-w" if platform.system().lower() == "windows" else "-W",
                 str(timeout * 1000 if platform.system().lower() == "windows" else timeout), host],
                capture_output=True, text=True, timeout=timeout + 2
            )
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def check_port(ip, port, timeout=1):
        """چک کردن یه پورت"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((ip, port))
                return result == 0
        except Exception:
            return False

    @staticmethod
    def scan_ports(ip, ports, progress_callback=None):
        """اسکن چند پورت"""
        results = []
        for i, port in enumerate(ports):
            is_open = NetworkScanner.check_port(ip, port)
            service = COMMON_PORTS.get(port, "Unknown")
            results.append({
                "port": port,
                "service": service,
                "status": "OPEN" if is_open else "closed"
            })
            if progress_callback:
                progress_callback(i + 1, len(ports), port, is_open)
        return results


# ============================================================
# اپلیکیشن گرافیکی
# ============================================================
class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" Network Scanner")
        self.root.geometry("950x700")
        self.root.configure(bg="#1e1e2e")

        self.db = ScanDB(DB_FILE)
        self.queue = queue.Queue()
        self.scanning = False

        self._build_ui()
        self._load_history()

    # --------------------------------------------------------
    # ساخت رابط کاربری
    # --------------------------------------------------------
    def _build_ui(self):
        # ===== هدر =====
        header = tk.Frame(self.root, bg="#1e1e2e")
        header.pack(fill="x", padx=10, pady=(10, 5))

        tk.Label(header, text=" Network Scanner", bg="#1e1e2e", fg="#00C2FF",
                 font=("Segoe UI", 16, "bold")).pack(side="left")

        self.status_label = tk.Label(header, text="Ready", bg="#1e1e2e",
                                     fg="#4CAF50", font=("Segoe UI", 10))
        self.status_label.pack(side="right")

        # ===== فرم =====
        form = tk.LabelFrame(self.root, text=" Target ",
                             bg="#1e1e2e", fg="#00C2FF",
                             font=("Segoe UI", 11, "bold"),
                             padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Host:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
        self.host_var = tk.StringVar(value="google.com")
        tk.Entry(form, textvariable=self.host_var, width=30,
                 font=("Segoe UI", 10)).grid(row=0, column=1, padx=5)

        tk.Label(form, text="Ports:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.ports_var = tk.StringVar(value="common")
        ttk.Combobox(form, textvariable=self.ports_var,
                     values=["common", "custom"], width=12,
                     state="readonly").grid(row=0, column=3, padx=5)
        self.ports_var.trace_add("write", self._toggle_custom_ports)

        self.custom_ports_var = tk.StringVar(value="80,443,22")
        self.custom_entry = tk.Entry(form, textvariable=self.custom_ports_var,
                                     width=20, font=("Segoe UI", 10),
                                     state="disabled")
        self.custom_entry.grid(row=0, column=4, padx=5)

        # ===== دکمه‌ها =====
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=5)

        self.scan_btn = self._make_btn(btn_frame, " Start Scan",
                                       self.start_scan, "#4CAF50")
        self._make_btn(btn_frame, " Stop", self.stop_scan, "#F44336")
        self._make_btn(btn_frame, " Export JSON", self.export_json, "#9C27B0")
        self._make_btn(btn_frame, " Clear", self.clear_results, "#607D8B")
        self._make_btn(btn_frame, " History", self._load_history, "#2196F3")

        # ===== Progress =====
        progress_frame = tk.Frame(self.root, bg="#1e1e2e")
        progress_frame.pack(fill="x", padx=10, pady=5)

        self.progress = ttk.Progressbar(progress_frame, mode="determinate")
        self.progress.pack(fill="x")

        self.progress_label = tk.Label(progress_frame, text="",
                                       bg="#1e1e2e", fg="#00C2FF",
                                       font=("Segoe UI", 9))
        self.progress_label.pack(anchor="w")

        # ===== نتایج =====
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # تب ۱: نتایج اسکن
        results_tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(results_tab, text=" Scan Results")

        columns = ("port", "service", "status", "banner")
        self.tree = ttk.Treeview(results_tab, columns=columns, show="headings")

        headings = {"port": "Port", "service": "Service",
                    "status": "Status", "banner": "Banner"}
        widths = {"port": 80, "service": 150, "status": 100, "banner": 500}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w")

        scrollbar = ttk.Scrollbar(results_tab, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # تب ۲: تاریخچه
        history_tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(history_tab, text=" History")

        hist_columns = ("id", "host", "ip", "time", "open", "total")
        self.history_tree = ttk.Treeview(history_tab, columns=hist_columns,
                                         show="headings")

        hist_headings = {"id": "ID", "host": "Host", "ip": "IP",
                         "time": "Time", "open": "Open Ports", "total": "Total"}
        hist_widths = {"id": 50, "host": 200, "ip": 130,
                       "time": 150, "open": 100, "total": 100}

        for col in hist_columns:
            self.history_tree.heading(col, text=hist_headings[col])
            self.history_tree.column(col, width=hist_widths[col], anchor="w")

        hist_scroll = ttk.Scrollbar(history_tab, orient="vertical",
                                    command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=hist_scroll.set)
        self.history_tree.pack(side="left", fill="both", expand=True)
        hist_scroll.pack(side="right", fill="y")

        self.history_tree.bind("<<TreeviewSelect>>", self._on_history_select)

        # ===== نوار وضعیت =====
        self.status_bar = tk.Label(self.root, text="Ready",
                                   bg="#2a2a3e", fg="#00C2FF",
                                   anchor="w", font=("Segoe UI", 9), padx=10)
        self.status_bar.pack(fill="x", side="bottom")

        # استایل Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2a2a3e", foreground="white",
                        fieldbackground="#2a2a3e", rowheight=26,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#00C2FF", foreground="black",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview",
                  background=[("selected", "#00C2FF")],
                  foreground=[("selected", "black")])

    def _make_btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                         relief="flat", cursor="hand2", width=14, pady=6)

    def _toggle_custom_ports(self, *args):
        if self.ports_var.get() == "custom":
            self.custom_entry.config(state="normal")
        else:
            self.custom_entry.config(state="disabled")

    # --------------------------------------------------------
    # عملیات اسکن
    # --------------------------------------------------------
    def get_ports(self):
        """لیست پورت‌ها بر اساس انتخاب کاربر"""
        if self.ports_var.get() == "common":
            return sorted(COMMON_PORTS.keys())
        try:
            return sorted(set(int(p.strip()) for p in self.custom_ports_var.get().split(",")))
        except ValueError:
            return sorted(COMMON_PORTS.keys())

    def start_scan(self):
        if self.scanning:
            messagebox.showwarning("Warning", "Scan already running!")
            return

        host = self.host_var.get().strip()
        if not host:
            messagebox.showwarning("Warning", "Enter a host!")
            return

        ports = self.get_ports()
        if not ports:
            messagebox.showwarning("Warning", "Enter valid ports!")
            return

        self.scanning = True
        self.scan_btn.config(state="disabled", bg="#666")
        self.status_label.config(text="Scanning...", fg="#FF9800")
        self.clear_results()

        # اجرا توی thread جداگانه
        thread = threading.Thread(target=self._scan_worker,
                                  args=(host, ports), daemon=True)
        thread.start()

        # شروع polling برای خوندن نتایج
        self.root.after(100, self._process_queue)

    def _scan_worker(self, host, ports):
        """کار اسکن توی thread جداگانه"""
        try:
            # ۱. Resolve
            self.queue.put(("status", f"Resolving {host}..."))
            ip = NetworkScanner.resolve_host(host)
            if not ip:
                self.queue.put(("error", f"Could not resolve {host}"))
                return

            self.queue.put(("status", f"IP: {ip}"))

            # ۲. Ping
            self.queue.put(("status", f"Pinging {ip}..."))
            ping_ok = NetworkScanner.ping(ip)
            self.queue.put(("status", f"Ping: {'✅' if ping_ok else '❌'}"))

            # ۳. ساخت رکورد اسکن
            scan_id = self.db.create_scan(host, ip, len(ports))
            self.queue.put(("scan_id", scan_id))

            # ۴. اسکن پورت‌ها
            open_count = 0
            for i, port in enumerate(ports):
                if not self.scanning:
                    break

                is_open = NetworkScanner.check_port(ip, port)
                service = COMMON_PORTS.get(port, "Unknown")
                status = "OPEN" if is_open else "closed"

                if is_open:
                    open_count += 1
                    self.db.add_port(scan_id, port, service, status)

                self.queue.put(("progress", i + 1, len(ports), port, is_open))

                # کمی صبر برای اینکه UI هنگ نکنه
                time.sleep(0.05)

            self.db.update_scan_count(scan_id, open_count)
            self.queue.put(("done", scan_id, open_count, len(ports)))

        except Exception as e:
            self.queue.put(("error", str(e)))

    def _process_queue(self):
        """پردازش نتایج توی thread اصلی (UI)"""
        try:
            while True:
                msg = self.queue.get_nowait()
                msg_type = msg[0]

                if msg_type == "status":
                    self.status_bar.config(text=msg[1])

                elif msg_type == "progress":
                    _, current, total, port, is_open = msg
                    self.progress["maximum"] = total
                    self.progress["value"] = current
                    status = "OPEN" if is_open else "closed"
                    color = "🟢" if is_open else "⚪"
                    self.progress_label.config(
                        text=f"{color} Port {port}: {status} ({current}/{total})"
                    )
                    if is_open:
                        service = COMMON_PORTS.get(port, "Unknown")
                        self.tree.insert("", "end",
                                         values=(port, service, status, "-"))

                elif msg_type == "scan_id":
                    self.current_scan_id = msg[1]

                elif msg_type == "done":
                    _, scan_id, open_count, total = msg
                    self.status_label.config(text=" Done", fg="#4CAF50")
                    self.status_bar.config(
                        text=f"Scan complete: {open_count}/{total} open ports"
                    )
                    self.scanning = False
                    self.scan_btn.config(state="normal", bg="#4CAF50")
                    self._load_history()
                    messagebox.showinfo("Scan Complete",
                                        f"Found {open_count} open ports out of {total}.")

                elif msg_type == "error":
                    self.status_label.config(text=" Error", fg="#F44336")
                    self.status_bar.config(text=f"Error: {msg[1]}")
                    self.scanning = False
                    self.scan_btn.config(state="normal", bg="#4CAF50")
                    messagebox.showerror("Error", msg[1])

        except queue.Empty:
            pass

        if self.scanning:
            self.root.after(100, self._process_queue)

    def stop_scan(self):
        if self.scanning:
            self.scanning = False
            self.status_label.config(text="Stopped", fg="#F44336")
            self.status_bar.config(text="Scan stopped by user")

    def clear_results(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.progress["value"] = 0
        self.progress_label.config(text="")

    # --------------------------------------------------------
    # تاریخچه
    # --------------------------------------------------------
    def _load_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        for row in self.db.get_history():
            self.history_tree.insert("", "end", values=row)

    def _on_history_select(self, event):
        selection = self.history_tree.selection()
        if not selection:
            return

        values = self.history_tree.item(selection[0], "values")
        scan_id = int(values[0])

        self.clear_results()
        for port, service, status in self.db.get_scan_details(scan_id):
            self.tree.insert("", "end", values=(port, service, status, "-"))

        self.status_bar.config(
            text=f"Loaded scan #{scan_id} ({values[1]})"
        )

    # --------------------------------------------------------
    # Export
    # --------------------------------------------------------
    def export_json(self):
        rows = self.tree.get_children()
        if not rows:
            messagebox.showwarning("Warning", "No results to export!")
            return

        data = []
        for row in rows:
            values = self.tree.item(row, "values")
            data.append({
                "port": int(values[0]),
                "service": values[1],
                "status": values[2],
            })

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "host": self.host_var.get(),
                        "scan_time": datetime.now().isoformat(),
                        "results": data
                    }, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Success", f"Exported to {file_path}")
            except IOError as e:
                messagebox.showerror("Error", str(e))


# ============================================================
# اجرا
# ============================================================
def main():
    root = tk.Tk()
    app = ScannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()