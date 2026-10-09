import sqlite3
import requests
import json
import logging
import time
from datetime import datetime
from pathlib import Path


# ============================================================
# تنظیمات
# ============================================================
DB_FILE = "github_data.db"
LOG_FILE = "pipeline.log"

# تنظیم لاگ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================
# ۱. ساخت دیتابیس
# ============================================================
def init_db():
    """ساخت جدول‌های لازم"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # جدول کاربران گیت‌هاب
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS github_users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            name TEXT,
            bio TEXT,
            public_repos INTEGER,
            followers INTEGER,
            following INTEGER,
            avatar_url TEXT,
            created_at TEXT,
            last_updated TEXT
        )
    """)

    # جدول لاگ اجراها
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_at TEXT,
            status TEXT,
            users_fetched INTEGER,
            errors INTEGER
        )
    """)

    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")


# ============================================================
# ۲. گرفتن داده از API
# ============================================================
def fetch_github_user(username):
    """گرفتن اطلاعات یه کاربر از GitHub API"""
    url = f"https://api.github.com/users/{username}"
    headers = {"User-Agent": "PythonPipeline/1.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            logger.warning(f"❌ User not found: {username}")
            return None
        elif response.status_code == 403:
            logger.error("⚠️ Rate limit exceeded. Wait a bit.")
            return None
        else:
            logger.error(f"❌ API error {response.status_code} for {username}")
            return None

    except requests.exceptions.Timeout:
        logger.error(f"⏱️ Timeout for {username}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"🌐 Network error for {username}: {e}")
        return None


# ============================================================
# ۳. اعتبارسنجی داده
# ============================================================
def validate_user(data):
    """چک کردن اینکه داده‌ی API معتبره"""
    if not data:
        return False
    required = ["id", "login"]
    return all(key in data for key in required)


# ============================================================
# ۴. ذخیره توی دیتابیس (Upsert)
# ============================================================
def save_user(conn, data):
    """ذخیره یا آپدیت کاربر توی دیتابیس"""
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO github_users
                (id, username, name, bio, public_repos, followers, following,
                 avatar_url, created_at, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                username = excluded.username,
                name = excluded.name,
                bio = excluded.bio,
                public_repos = excluded.public_repos,
                followers = excluded.followers,
                following = excluded.following,
                avatar_url = excluded.avatar_url,
                last_updated = excluded.last_updated
        """, (
            data["id"],
            data["login"],
            data.get("name"),
            data.get("bio"),
            data.get("public_repos", 0),
            data.get("followers", 0),
            data.get("following", 0),
            data.get("avatar_url"),
            data.get("created_at"),
            now
        ))
        conn.commit()
        logger.info(f"💾 Saved: {data['login']} ({data.get('name') or 'no name'})")
        return True

    except sqlite3.Error as e:
        logger.error(f"❌ DB error for {data['login']}: {e}")
        return False


# ============================================================
# ۵. خط لوله اصلی
# ============================================================
def run_pipeline(usernames):
    """اجرای خط لوله: API → Validation → DB"""
    logger.info("=" * 50)
    logger.info(f"🚀 Pipeline started ({len(usernames)} users)")
    logger.info("=" * 50)

    conn = sqlite3.connect(DB_FILE)
    fetched = 0
    errors = 0

    for i, username in enumerate(usernames, 1):
        logger.info(f"[{i}/{len(usernames)}] Fetching: {username}")

        # ۱. گرفتن از API
        data = fetch_github_user(username)

        # ۲. اعتبارسنجی
        if not validate_user(data):
            errors += 1
            continue

        # ۳. ذخیره توی DB
        if save_user(conn, data):
            fetched += 1
        else:
            errors += 1

        # ۴. احترام به Rate Limit (۶۰ درخواست در ساعت برای غیراحراز هویت)
        time.sleep(1)

    # ثبت نتیجه‌ی اجرا
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pipeline_runs (run_at, status, users_fetched, errors)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "success" if errors == 0 else "partial",
        fetched,
        errors
    ))
    conn.commit()
    conn.close()

    logger.info("=" * 50)
    logger.info(f"✅ Pipeline finished: {fetched} saved, {errors} errors")
    logger.info("=" * 50)


# ============================================================
# ۶. گزارش‌گیری
# ============================================================
def show_report():
    """نمایش گزارش از دیتابیس"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("\n" + "=" * 60)
    print("📊 GITHUB USERS REPORT")
    print("=" * 60)

    cursor.execute("""
        SELECT username, name, public_repos, followers
        FROM github_users
        ORDER BY followers DESC
    """)
    rows = cursor.fetchall()

    if not rows:
        print("📭 No data yet.")
    else:
        print(f"{'Username':<20} {'Name':<25} {'Repos':<8} {'Followers'}")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]:<20} {(row[1] or '-')[:24]:<25} {row[2]:<8} {row[3]}")

    # آمار کلی
    cursor.execute("SELECT COUNT(*), SUM(public_repos), SUM(followers) FROM github_users")
    total, repos, followers = cursor.fetchone()
    print("\n📈 TOTALS:")
    print(f"   Users: {total or 0}")
    print(f"   Total repos: {repos or 0}")
    print(f"   Total followers: {followers or 0}")

    # آخرین اجرا
    cursor.execute("""
        SELECT run_at, status, users_fetched, errors
        FROM pipeline_runs ORDER BY id DESC LIMIT 1
    """)
    last_run = cursor.fetchone()
    if last_run:
        print(f"\n🕐 LAST RUN: {last_run[0]} | Status: {last_run[1]} | "
              f"Fetched: {last_run[2]} | Errors: {last_run[3]}")

    conn.close()
    print("=" * 60 + "\n")


# ============================================================
# ۷. پاک کردن داده‌های قدیمی
# ============================================================
def cleanup_old_data(days=30):
    """حذف کاربرانی که بیش از X روز آپدیت نشدن"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM github_users
        WHERE last_updated < datetime('now', ?)
    """, (f"-{days} days",))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    logger.info(f"🧹 Cleaned up {deleted} old records")


# ============================================================
# ۸. Export به JSON
# ============================================================
def export_to_json(filename="github_users.json"):
    """خروجی گرفتن همه‌ی کاربران به JSON"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM github_users")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    data = [dict(zip(columns, row)) for row in rows]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"💾 Exported {len(data)} users to {filename}")


# ============================================================
# منوی اصلی
# ============================================================
def main():
    init_db()

    print("=" * 50)
    print("🔗 GitHub Data Pipeline")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Fetch users (run pipeline)")
        print("2. Show report")
        print("3. Add custom usernames to fetch")
        print("4. Cleanup old data")
        print("5. Export to JSON")
        print("6. Exit")

        choice = input("\nChoose (1-6): ").strip()

        if choice == "1":
            default_users = [
                "torvalds", "gvanrossum", "yasminebrahimi2006",
                "microsoft", "google", "python"
            ]
            run_pipeline(default_users)
            show_report()

        elif choice == "2":
            show_report()

        elif choice == "3":
            raw = input("Usernames (comma-separated): ").strip()
            usernames = [u.strip() for u in raw.split(",") if u.strip()]
            if usernames:
                run_pipeline(usernames)
                show_report()

        elif choice == "4":
            try:
                days = int(input("Delete records older than (days): ").strip())
                cleanup_old_data(days)
            except ValueError:
                print("❌ Invalid number.")

        elif choice == "5":
            export_to_json()

        elif choice == "6":
            print("Bye! 👋")
            break

        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()