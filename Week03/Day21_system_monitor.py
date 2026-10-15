import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import sqlite3
import platform
import threading
import time
from datetime import datetime
from collections import deque


DB_FILE = "monitor.db"
HISTORY_SIZE = 60  # 60 نقطه روی نمودار


# ============================================================
# دیتابیس
# ============================================================
class MonitorDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                cpu REAL,
                ram REAL,
                disk REAL
            )
        """)
        self.conn.commit()

    def log_metrics(self, cpu, ram, disk):
        self.cursor.execute("""
            INSERT INTO metrics (timestamp, cpu, ram, disk)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cpu, ram, disk))
        self.conn.commit()

    def get_recent(self, limit=10):
        self.cursor.execute("""
            SELECT timestamp, cpu, ram, disk
            FROM metrics ORDER BY id DESC LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def get_stats(self):
        self.cursor.execute("""
            SELECT
                COUNT(*),
                AVG(cpu), MAX(cpu),
                AVG(ram), MAX(ram),
                AVG(disk), MAX(disk)
            FROM metrics
        """)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()


# ============================================================
# جمع‌آوری اطلاعات سیستم
# ============================================================
def get_system_info():
    """اطلاعات کلی سیستم"""
    try:
        cpu_freq = psutil.cpu_freq()
        freq_str = f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A"
    except Exception:
        freq_str = "N/A"

    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "OS": f"{platform.system()} {platform.release()}",
        "Machine": platform.machine(),
        "Processor": platform.processor() or "N/A",
        "CPU Cores": f"{psutil.cpu_count(logical=False)} physical / "
                     f"{psutil.cpu_count(logical=True)} logical",
        "CPU Freq": freq_str,
        "Total RAM": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        "Total Disk": f"{psutil.disk_usage('/').total / (1024**3):.2f} GB",
        "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M"),
        "Uptime": f"{hours}h {minutes}m {seconds}s",
        "Python": platform.python_version(),
    }


# ============================================================
# اپلیکیشن گرافیکی
# ============================================================
class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖥️ System Monitor")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1e1e2e")

        self.db = MonitorDB(DB_FILE)
        self.cpu_history = deque([0] * HISTORY_SIZE, maxlen=HISTORY_SIZE)
        self.ram_history = deque([0] * HISTORY_SIZE, maxlen=HISTORY_SIZE)
        self.running = True
        self.last_db_log = 0  # زمان آخرین لاگ توی دیتابیس

        self._build_ui()
        self._update_loop()

    # --------------------------------------------------------
    # رابط کاربری
    # --------------------------------------------------------
    def _build_ui(self):
        # ===== هدر =====
        header = tk.Frame(self.root, bg="#1e1e2e")
        header.pack(fill="x", padx=10, pady=(10, 5))

        tk.Label(header, text="🖥️ System Monitor", bg="#1e1e2e",
                 fg="#00C2FF", font=("Segoe UI", 16, "bold")).pack(side="left")

        self.status_label = tk.Label(header, text="● Live", bg="#1e1e2e",
                                     fg="#4CAF50", font=("Segoe UI", 10, "bold"))
        self.status_label.pack(side="right", padx=10)

        # ===== کارت‌های آماری =====
        cards_frame = tk.Frame(self.root, bg="#1e1e2e")
        cards_frame.pack(fill="x", padx=10, pady=5)

        self.cpu_card = self._make_stat_card(cards_frame, "CPU", "0%", "#4CAF50")
        self.ram_card = self._make_stat_card(cards_frame, "RAM", "0%", "#2196F3")
        self.disk_card = self._make_stat_card(cards_frame, "DISK", "0%", "#FF9800")

        # ===== نمودار =====
        chart_frame = tk.LabelFrame(self.root, text=" Live Usage ",
                                    bg="#1e1e2e", fg="#00C2FF",
                                    font=("Segoe UI", 11, "bold"),
                                    padx=10, pady=10)
        chart_frame.pack(fill="x", padx=10, pady=5)

        self.canvas = tk.Canvas(chart_frame, bg="#0d0d1a",
                                height=180, highlightthickness=0)
        self.canvas.pack(fill="x")

        # ===== Notebook =====
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # تب پروسه‌ها
        proc_tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(proc_tab, text=" Processes")

        proc_top = tk.Frame(proc_tab, bg="#1e1e2e")
        proc_top.pack(fill="x", padx=5, pady=5)

        self.proc_filter = tk.StringVar()
        self.proc_filter.trace_add("write", lambda *a: self._refresh_processes())
        tk.Label(proc_top, text=" Filter:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 10)).pack(side="left")
        tk.Entry(proc_top, textvariable=self.proc_filter,
                 font=("Segoe UI", 10), width=30).pack(side="left", padx=5)

        tk.Button(proc_top, text=" Refresh", command=self._refresh_processes,
                  bg="#2196F3", fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side="right")

        tk.Button(proc_top, text=" Kill", command=self._kill_process,
                  bg="#F44336", fg="white", relief="flat",
                  font=("Segoe UI", 9, "bold"), cursor="hand2").pack(side="right", padx=5)

        columns = ("pid", "name", "cpu", "ram", "status", "user")
        self.proc_tree = ttk.Treeview(proc_tab, columns=columns, show="headings")

        headings = {"pid": "PID", "name": "Name", "cpu": "CPU %",
                    "ram": "RAM (MB)", "status": "Status", "user": "User"}
        widths = {"pid": 70, "name": 250, "cpu": 80,
                  "ram": 100, "status": 100, "user": 150}

        for col in columns:
            self.proc_tree.heading(col, text=headings[col],
                                   command=lambda c=col: self._sort_processes(c))
            self.proc_tree.column(col, width=widths[col], anchor="w")

        proc_scroll = ttk.Scrollbar(proc_tab, orient="vertical",
                                    command=self.proc_tree.yview)
        self.proc_tree.configure(yscrollcommand=proc_scroll.set)
        self.proc_tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        proc_scroll.pack(side="right", fill="y", pady=5)

        # تب اطلاعات سیستم
        info_tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(info_tab, text=" System Info")

        self.info_text = tk.Text(info_tab, bg="#2a2a3e", fg="white",
                                 font=("Consolas", 11), wrap="word",
                                 padx=15, pady=15, relief="flat")
        self.info_text.pack(fill="both", expand=True, padx=5, pady=5)

        info = get_system_info()
        for key, value in info.items():
            self.info_text.insert("end", f"{key:<15}: {value}\n")
        self.info_text.config(state="disabled")

        # تب تاریخچه
        history_tab = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(history_tab, text=" History")

        hist_columns = ("time", "cpu", "ram", "disk")
        self.hist_tree = ttk.Treeview(history_tab, columns=hist_columns,
                                      show="headings")

        hist_headings = {"time": "Time", "cpu": "CPU %",
                         "ram": "RAM %", "disk": "Disk %"}
        for col in hist_columns:
            self.hist_tree.heading(col, text=hist_headings[col])
            self.hist_tree.column(col, width=180, anchor="center")

        hist_scroll = ttk.Scrollbar(history_tab, orient="vertical",
                                    command=self.hist_tree.yview)
        self.hist_tree.configure(yscrollcommand=hist_scroll.set)
        self.hist_tree.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        hist_scroll.pack(side="right", fill="y", pady=5)

        # ===== نوار وضعیت =====
        self.status_bar = tk.Label(self.root, text="Ready",
                                   bg="#2a2a3e", fg="#00C2FF",
                                   anchor="w", font=("Segoe UI", 9), padx=10)
        self.status_bar.pack(fill="x", side="bottom")

        # استایل
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

    def _make_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="#2a2a3e", padx=15, pady=15)
        card.pack(side="left", fill="x", expand=True, padx=5)

        tk.Label(card, text=title, bg="#2a2a3e", fg=color,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        val_label = tk.Label(card, text=value, bg="#2a2a3e", fg="white",
                             font=("Segoe UI", 22, "bold"))
        val_label.pack(anchor="w")
        sub_label = tk.Label(card, text="", bg="#2a2a3e", fg="#888",
                             font=("Segoe UI", 9))
        sub_label.pack(anchor="w")
        card.value_label = val_label
        card.sub_label = sub_label
        return card

    # --------------------------------------------------------
    # به‌روزرسانی زنده
    # --------------------------------------------------------
    def _update_loop(self):
        """حلقه‌ی اصلی به‌روزرسانی"""
        if not self.running:
            return

        try:
            # CPU
            cpu = psutil.cpu_percent(interval=None)
            # RAM
            ram = psutil.virtual_memory().percent
            ram_used = psutil.virtual_memory().used / (1024**3)
            ram_total = psutil.virtual_memory().total / (1024**3)
            # Disk
            disk = psutil.disk_usage('/').percent
            disk_used = psutil.disk_usage('/').used / (1024**3)
            disk_total = psutil.disk_usage('/').total / (1024**3)

            # کارت‌ها
            self.cpu_card.value_label.config(text=f"{cpu:.1f}%")
            self.cpu_card.sub_label.config(text=f"{psutil.cpu_count()} cores")

            self.ram_card.value_label.config(text=f"{ram:.1f}%")
            self.ram_card.sub_label.config(
                text=f"{ram_used:.1f} / {ram_total:.1f} GB"
            )

            self.disk_card.value_label.config(text=f"{disk:.1f}%")
            self.disk_card.sub_label.config(
                text=f"{disk_used:.1f} / {disk_total:.1f} GB"
            )

            # تاریخچه‌ی نمودار
            self.cpu_history.append(cpu)
            self.ram_history.append(ram)
            self._draw_chart()

            # ذخیره توی دیتابیس (هر ۵ ثانیه)
            now = time.time()
            if now - self.last_db_log >= 5:
                self.db.log_metrics(cpu, ram, disk)
                self.last_db_log = now
                self._refresh_history()

        except Exception as e:
            self.status_bar.config(text=f"Error: {e}")

        self.root.after(1000, self._update_loop)

    def _draw_chart(self):
        """رسم نمودار زنده"""
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w < 10 or h < 10:
            return

        # خطوط راهنما
        for i in range(1, 4):
            y = h * i / 4
            self.canvas.create_line(0, y, w, y, fill="#333", dash=(3, 3))
            self.canvas.create_text(5, y - 8, text=f"{100 - i*25}%",
                                    fill="#666", anchor="w",
                                    font=("Segoe UI", 8))

        # تابع رسم
        def draw_line(data, color):
            if len(data) < 2:
                return
            points = []
            step = w / (HISTORY_SIZE - 1)
            for i, val in enumerate(data):
                x = i * step
                y = h - (val / 100) * h
                points.extend([x, y])
            if len(points) >= 4:
                self.canvas.create_line(*points, fill=color, width=2,
                                        smooth=True)

        draw_line(self.cpu_history, "#4CAF50")
        draw_line(self.ram_history, "#2196F3")

        # راهنما
        self.canvas.create_text(w - 100, 15, text="● CPU", fill="#4CAF50",
                                anchor="w", font=("Segoe UI", 10, "bold"))
        self.canvas.create_text(w - 100, 35, text="● RAM", fill="#2196F3",
                                anchor="w", font=("Segoe UI", 10, "bold"))

    # --------------------------------------------------------
    # پروسه‌ها
    # --------------------------------------------------------
    def _refresh_processes(self):
        """به‌روزرسانی لیست پروسه‌ها"""
        for row in self.proc_tree.get_children():
            self.proc_tree.delete(row)

        keyword = self.proc_filter.get().lower()
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent',
                                          'memory_info', 'status', 'username']):
            try:
                info = proc.info
                name = info['name'] or "Unknown"

                if keyword and keyword not in name.lower():
                    continue

                cpu = info['cpu_percent'] or 0
                ram = (info['memory_info'].rss / (1024**2)) if info['memory_info'] else 0

                processes.append((
                    info['pid'], name, f"{cpu:.1f}", f"{ram:.1f}",
                    info['status'] or "-", (info['username'] or "-")[:20]
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # مرتب‌سازی بر اساس CPU
        processes.sort(key=lambda x: float(x[2]), reverse=True)

        for p in processes[:50]:
            self.proc_tree.insert("", "end", values=p)

        self.status_bar.config(text=f"📋 {len(processes)} processes running")

    def _sort_processes(self, column):
        """مرتب‌سازی بر اساس ستون"""
        items = [(self.proc_tree.set(k, column), k)
                 for k in self.proc_tree.get_children("")]
        try:
            items.sort(key=lambda t: float(t[0]), reverse=True)
        except ValueError:
            items.sort(key=lambda t: t[0].lower(), reverse=False)

        for index, (_, k) in enumerate(items):
            self.proc_tree.move(k, "", index)

    def _kill_process(self):
        """کشتن پروسه‌ی انتخاب‌شده"""
        selection = self.proc_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Select a process first!")
            return

        values = self.proc_tree.item(selection[0], "values")
        pid = int(values[0])
        name = values[1]

        if not messagebox.askyesno("Confirm",
                                   f"Kill process '{name}' (PID {pid})?"):
            return

        try:
            proc = psutil.Process(pid)
            proc.terminate()
            self.status_bar.config(text=f" Killed {name} (PID {pid})")
            self.root.after(500, self._refresh_processes)
        except psutil.AccessDenied:
            messagebox.showerror("Error", "Access denied. Run as admin.")
        except psutil.NoSuchProcess:
            messagebox.showerror("Error", "Process no longer exists.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------------
    # تاریخچه
    # --------------------------------------------------------
    def _refresh_history(self):
        for row in self.hist_tree.get_children():
            self.hist_tree.delete(row)

        for row in self.db.get_recent(50):
            time_str, cpu, ram, disk = row
            self.hist_tree.insert("", "end",
                                  values=(time_str, f"{cpu:.1f}",
                                          f"{ram:.1f}", f"{disk:.1f}"))


# ============================================================
# اجرا
# ============================================================
def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()