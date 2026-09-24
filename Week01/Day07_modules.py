# ============ بخش ۱: ماژول‌های داخلی ============

# --- os ---
import os
print("=== OS ===")
print("مسیر فعلی:", os.getcwd())
print("فایل‌های پوشه:")
for item in os.listdir(".")[:5]:
    print(f"  - {item}")

# --- sys ---
import sys
print("\n=== SYS ===")
print("نسخه پایتون:", sys.version.split()[0])

# --- datetime ---
from datetime import datetime, timedelta
print("\n=== DATETIME ===")
now = datetime.now()
print("الان:", now.strftime("%Y-%m-%d %H:%M:%S"))
print("فردا:", (now + timedelta(days=1)).strftime("%Y-%m-%d"))

# --- random ---
import random
print("\n=== RANDOM ===")
print("عدد تصادفی:", random.randint(1, 100))
print("انتخاب تصادفی:", random.choice(["Ali", "Sara", "Reza"]))

# --- math ---
import math
print("\n=== MATH ===")
print("π:", math.pi)
print("جذر ۱۶:", math.sqrt(16))
print("توان ۲^۱۰:", math.pow(2, 10))

# --- json ---
import json
print("\n=== JSON ===")
data = {"name": "Yasmin", "age": 20, "skills": ["Python", "Network"]}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print(json_str)

# --- socket ---
import socket
print("\n=== SOCKET ===")
sites = ["google.com", "github.com", "python.org"]
for site in sites:
    try:
        ip = socket.gethostbyname(site)
        print(f"{site} → {ip}")
    except socket.gaierror:
        print(f"{site} → پیدا نشد")

# --- subprocess ---
import subprocess
print("\n=== SUBPROCESS ===")
try:
    result = subprocess.run(["ping", "-n", "1", "8.8.8.8"],
                            capture_output=True, text=True, timeout=5)
    print("پینگ موفق!" if result.returncode == 0 else "پینگ ناموفق")
except Exception as e:
    print(f"خطا: {e}")

# ============ بخش ۲: import با اسم مستعار ============
import math as m
print("\n=== ALIAS ===")
print("π با alias:", m.pi)

# ============ بخش ۳: import بخشی ============
from math import pi, sqrt
print("\n=== PARTIAL IMPORT ===")
print("π:", pi)
print("√۲۵:", sqrt(25))

# ============ تمرین‌ها ============
print("\n=== تمرین‌ها ===")

# تمرین ۱: os
print("\n۱. مسیر فعلی:", os.getcwd())

# تمرین ۲: datetime
now = datetime.now()
print(f"۲. تاریخ: {now.strftime('%Y-%m-%d')}، روز: {now.strftime('%A')}")

# تمرین ۳: random
numbers = [random.randint(1, 100) for _ in range(5)]
print(f"۳. اعداد تصادفی: {numbers}")

# تمرین ۴: socket
try:
    ip = socket.gethostbyname("github.com")
    print(f"۴. GitHub IP: {ip}")
except:
    print("۴. خطا در اتصال")

# تمرین ۵: ساخت ماژول (فایل جداگانه)
print("\n۵. ماژول network_utils.py ساخته شد")


# ============================================
# نکات مهم تاپل (Tuple)
# ============================================
# - غیرقابل تغییر: بعد از ساختن، نمی‌تونی عوضش کنی
# - سریع‌تر از لیست: چون تغییرناپذیره
# - برای داده‌های ثابت: مثل مختصات، تاریخ
# - تک‌عضوی: حتماً کاما بذار: (5,)

# ============================================
# نکات مهم ست (Set)
# ============================================
# - بدون ترتیب: ایندکس نداره
# - بدون تکرار: عالی برای حذف تکراری‌ها
# - عملیات ریاضی: اشتراک، اجتماع، تفاضل
# - سریع: جستجو توش خیلی سریعه

# ============================================
# اشتباهات رایج
# ============================================
# - (5) تاپل نیست، عدده. (5,) تاپله.
# - {} ست نیست، دیکشنریه. set() برای ست خالیه.
# - ست ایندکس نداره، پس set[0] خطا میده.