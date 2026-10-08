import sqlite3
import os
from datetime import datetime


DB_FILE = "contacts.db"


# ============================================================
# ۱. اتصال به دیتابیس
# ============================================================
def connect():
    """اتصال به دیتابیس و ساخت جدول اگه وجود نداشت"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    return conn


# ============================================================
# ۲. اضافه کردن مخاطب (INSERT)
# ============================================================
def add_contact(conn, name, phone, email=""):
    """اضافه کردن یه مخاطب جدید"""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (name, phone, email, created_at)
        VALUES (?, ?, ?, ?)
    """, (name, phone, email, datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    print(f" Contact '{name}' added (ID: {cursor.lastrowid})")
    return cursor.lastrowid


# ============================================================
# ۳. خواندن همه‌ی مخاطبین (SELECT)
# ============================================================
def list_contacts(conn):
    """نمایش همه‌ی مخاطبین"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, email, created_at FROM contacts ORDER BY name")
    rows = cursor.fetchall()

    if not rows:
        print("📭 No contacts found.")
        return

    print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15} {'Email':<25} {'Created'}")
    print("-" * 85)
    for row in rows:
        id_, name, phone, email, created = row
        print(f"{id_:<5} {name:<20} {phone:<15} {email or '-':<25} {created}")


# ============================================================
# ۴. جستجو (SELECT with WHERE)
# ============================================================
def search_contacts(conn, keyword):
    """جستجو توی اسم، شماره، یا ایمیل"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, phone, email FROM contacts
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    return cursor.fetchall()


# ============================================================
# ۵. ویرایش مخاطب (UPDATE)
# ============================================================
def update_contact(conn, contact_id, name=None, phone=None, email=None):
    """ویرایش یه مخاطب"""
    cursor = conn.cursor()

    # اول چک کن وجود داره
    cursor.execute("SELECT id FROM contacts WHERE id = ?", (contact_id,))
    if not cursor.fetchone():
        print(f"❌ Contact with ID {contact_id} not found.")
        return

    # آپدیت فقط فیلدهایی که داده شدن
    if name:
        cursor.execute("UPDATE contacts SET name = ? WHERE id = ?", (name, contact_id))
    if phone:
        cursor.execute("UPDATE contacts SET phone = ? WHERE id = ?", (phone, contact_id))
    if email:
        cursor.execute("UPDATE contacts SET email = ? WHERE id = ?", (email, contact_id))

    conn.commit()
    print(f" Contact {contact_id} updated.")


# ============================================================
# ۶. حذف مخاطب (DELETE)
# ============================================================
def delete_contact(conn, contact_id):
    """حذف یه مخاطب"""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"🗑️  Contact {contact_id} deleted.")
    else:
        print(f"❌ Contact {contact_id} not found.")


# ============================================================
# ۷. شمارش مخاطبین (COUNT)
# ============================================================
def count_contacts(conn):
    """تعداد کل مخاطبین"""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM contacts")
    return cursor.fetchone()[0]


# ============================================================
# ۸. گروه‌بندی بر اساس حرف اول (GROUP BY)
# ============================================================
def contacts_by_letter(conn):
    """گروه‌بندی مخاطبین بر اساس حرف اول اسم"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT UPPER(SUBSTR(name, 1, 1)) AS letter, COUNT(*) AS count
        FROM contacts
        GROUP BY letter
        ORDER BY letter
    """)
    return cursor.fetchall()


# ============================================================
# ۹. خروجی گرفتن به CSV
# ============================================================
def export_to_csv(conn, filename="contacts.csv"):
    """ذخیره‌ی همه‌ی مخاطبین توی فایل CSV"""
    import csv
    cursor = conn.cursor()
    cursor.execute("SELECT name, phone, email, created_at FROM contacts")
    rows = cursor.fetchall()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Created"])
        writer.writerows(rows)

    print(f"💾 Exported {len(rows)} contacts to {filename}")


# ============================================================
# منوی اصلی
# ============================================================
def main():
    conn = connect()

    print("=" * 50)
    print("📇 Contact Manager (SQLite)")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Add contact")
        print("2. List all contacts")
        print("3. Search contacts")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Count contacts")
        print("7. Contacts by letter")
        print("8. Export to CSV")
        print("9. Exit")

        choice = input("\nChoose (1-9): ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email (optional): ").strip()
            if name and phone:
                add_contact(conn, name, phone, email)
            else:
                print("❌ Name and phone are required.")

        elif choice == "2":
            list_contacts(conn)

        elif choice == "3":
            keyword = input("Search (name/phone/email): ").strip()
            results = search_contacts(conn, keyword)
            if results:
                for row in results:
                    print(f"  {row[0]}. {row[1]} | {row[2]} | {row[3] or '-'}")
            else:
                print("📭 No results.")

        elif choice == "4":
            try:
                cid = int(input("Contact ID: ").strip())
                print("(Leave blank to skip a field)")
                name = input("New name: ").strip() or None
                phone = input("New phone: ").strip() or None
                email = input("New email: ").strip() or None
                update_contact(conn, cid, name, phone, email)
            except ValueError:
                print(" Invalid ID.")

        elif choice == "5":
            try:
                cid = int(input("Contact ID: ").strip())
                confirm = input(f"Delete contact {cid}? (y/n): ").strip().lower()
                if confirm == "y":
                    delete_contact(conn, cid)
            except ValueError:
                print(" Invalid ID.")

        elif choice == "6":
            print(f" Total contacts: {count_contacts(conn)}")

        elif choice == "7":
            groups = contacts_by_letter(conn)
            for letter, count in groups:
                print(f"  {letter}: {'█' * count} ({count})")

        elif choice == "8":
            export_to_csv(conn)

        elif choice == "9":
            conn.close()
            print("Bye! ")
            break

        else:
            print(" Invalid choice.")


if __name__ == "__main__":
    main()