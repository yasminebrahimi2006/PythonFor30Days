import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


DB_FILE = "contacts_gui.db"


# ============================================================
# دیتابیس
# ============================================================
class ContactDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                category TEXT,
                created_at TEXT
            )
        """)
        self.conn.commit()

    def add(self, name, phone, email, category):
        self.cursor.execute("""
            INSERT INTO contacts (name, phone, email, category, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, email, category,
              datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, cid, name, phone, email, category):
        self.cursor.execute("""
            UPDATE contacts
            SET name = ?, phone = ?, email = ?, category = ?
            WHERE id = ?
        """, (name, phone, email, category, cid))
        self.conn.commit()
        return self.cursor.rowcount

    def delete(self, cid):
        self.cursor.execute("DELETE FROM contacts WHERE id = ?", (cid,))
        self.conn.commit()
        return self.cursor.rowcount

    def get_all(self, search=""):
        if search:
            self.cursor.execute("""
                SELECT id, name, phone, email, category, created_at
                FROM contacts
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                ORDER BY name
            """, (f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            self.cursor.execute("""
                SELECT id, name, phone, email, category, created_at
                FROM contacts ORDER BY name
            """)
        return self.cursor.fetchall()

    def get_by_id(self, cid):
        self.cursor.execute("SELECT * FROM contacts WHERE id = ?", (cid,))
        return self.cursor.fetchone()

    def count(self):
        self.cursor.execute("SELECT COUNT(*) FROM contacts")
        return self.cursor.fetchone()[0]

    def close(self):
        self.conn.close()


# ============================================================
# اپلیکیشن گرافیکی
# ============================================================
class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title(" Contact Manager")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2e")

        self.db = ContactDB(DB_FILE)
        self.selected_id = None

        self._build_ui()
        self.refresh_list()

    # --------------------------------------------------------
    # ساخت رابط کاربری
    # --------------------------------------------------------
    def _build_ui(self):
        # ===== بخش جستجو =====
        search_frame = tk.Frame(self.root, bg="#1e1e2e")
        search_frame.pack(fill="x", padx=10, pady=(10, 5))

        tk.Label(search_frame, text=" Search:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 11)).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self.refresh_list())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                font=("Segoe UI", 11))
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # ===== بخش فرم =====
        form_frame = tk.LabelFrame(self.root, text=" Contact Info ",
                                   bg="#1e1e2e", fg="#00C2FF",
                                   font=("Segoe UI", 11, "bold"),
                                   padx=10, pady=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        # Name
        tk.Label(form_frame, text="Name:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.name_var,
                 font=("Segoe UI", 10), width=30).grid(row=0, column=1, padx=5, pady=3)

        # Phone
        tk.Label(form_frame, text="Phone:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.phone_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.phone_var,
                 font=("Segoe UI", 10), width=20).grid(row=0, column=3, padx=5, pady=3)

        # Email
        tk.Label(form_frame, text="Email:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.email_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.email_var,
                 font=("Segoe UI", 10), width=30).grid(row=1, column=1, padx=5, pady=3)

        # Category
        tk.Label(form_frame, text="Category:", bg="#1e1e2e", fg="white",
                 font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w", padx=5, pady=3)
        self.category_var = tk.StringVar(value="Family")
        category_menu = ttk.Combobox(form_frame, textvariable=self.category_var,
                                     values=["Family", "Friend", "Work", "Other"],
                                     font=("Segoe UI", 10), width=17, state="readonly")
        category_menu.grid(row=1, column=3, padx=5, pady=3)

        # ===== دکمه‌ها =====
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=5)

        self._make_btn(btn_frame, " Add", self.add_contact, "#4CAF50")
        self._make_btn(btn_frame, " Update", self.update_contact, "#FF9800")
        self._make_btn(btn_frame, " Delete", self.delete_contact, "#F44336")
        self._make_btn(btn_frame, " Clear", self.clear_form, "#607D8B")
        self._make_btn(btn_frame, " Refresh", self.refresh_list, "#2196F3")

        # ===== جدول =====
        table_frame = tk.Frame(self.root, bg="#1e1e2e")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2a2a3e",
                        foreground="white",
                        fieldbackground="#2a2a3e",
                        rowheight=28,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#00C2FF",
                        foreground="black",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#00C2FF")],
                  foreground=[("selected", "black")])

        columns = ("id", "name", "phone", "email", "category", "created")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        headings = {
            "id": "ID", "name": "Name", "phone": "Phone",
            "email": "Email", "category": "Category", "created": "Created"
        }
        widths = {"id": 50, "name": 180, "phone": 130,
                  "email": 200, "category": 100, "created": 130}

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ===== نوار وضعیت =====
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var,
                              bg="#2a2a3e", fg="#00C2FF",
                              anchor="w", font=("Segoe UI", 9), padx=10)
        status_bar.pack(fill="x", side="bottom")

    def _make_btn(self, parent, text, cmd, color):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                         relief="flat", cursor="hand2", width=12, pady=5
                         ).pack(side="left", padx=3)

    # --------------------------------------------------------
    # عملیات
    # --------------------------------------------------------
    def refresh_list(self):
        """به‌روزرسانی جدول"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        search = self.search_var.get()
        rows = self.db.get_all(search)

        for row in rows:
            self.tree.insert("", "end", values=row)

        self.status_var.set(f" {len(rows)} contacts | Total: {self.db.count()}")

    def on_select(self, event):
        """وقتی روی یه ردیف کلیک میشه"""
        selection = self.tree.selection()
        if not selection:
            return

        values = self.tree.item(selection[0], "values")
        self.selected_id = int(values[0])

        self.name_var.set(values[1])
        self.phone_var.set(values[2])
        self.email_var.set(values[3])
        self.category_var.set(values[4])

    def clear_form(self):
        """پاک کردن فرم"""
        self.selected_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.category_var.set("Family")
        self.tree.selection_remove(self.tree.selection())

    def validate_form(self):
        """اعتبارسنجی فرم"""
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name:
            messagebox.showwarning("Warning", "Name is required!")
            return False
        if not phone:
            messagebox.showwarning("Warning", "Phone is required!")
            return False
        if not phone.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            messagebox.showwarning("Warning", "Phone must contain only digits!")
            return False
        return True

    def add_contact(self):
        if not self.validate_form():
            return

        self.db.add(
            self.name_var.get().strip(),
            self.phone_var.get().strip(),
            self.email_var.get().strip(),
            self.category_var.get()
        )
        self.refresh_list()
        self.clear_form()
        self.status_var.set(" Contact added!")
        messagebox.showinfo("Success", "Contact added!")

    def update_contact(self):
        if self.selected_id is None:
            messagebox.showwarning("Warning", "Select a contact first!")
            return
        if not self.validate_form():
            return

        self.db.update(
            self.selected_id,
            self.name_var.get().strip(),
            self.phone_var.get().strip(),
            self.email_var.get().strip(),
            self.category_var.get()
        )
        self.refresh_list()
        self.clear_form()
        self.status_var.set(" Contact updated!")
        messagebox.showinfo("Success", "Contact updated!")

    def delete_contact(self):
        if self.selected_id is None:
            messagebox.showwarning("Warning", "Select a contact first!")
            return

        name = self.name_var.get()
        if not messagebox.askyesno("Confirm", f"Delete '{name}'?"):
            return

        self.db.delete(self.selected_id)
        self.refresh_list()
        self.clear_form()
        self.status_var.set(" Contact deleted!")
        messagebox.showinfo("Success", "Contact deleted!")


# ============================================================
# اجرا
# ============================================================
def main():
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()