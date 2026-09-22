import re

# ============================================
# بخش ۱: کار با رشته‌ها (Strings)
# ============================================

text = "Hello, Network Engineer!"

# طول رشته
print("طول:", len(text))

# حروف بزرگ و کوچک
print("بزرگ:", text.upper())
print("کوچک:", text.lower())

# حذف فاصله‌های اضافی
spaced = "   hello   "
print("حذف فاصله:", spaced.strip())

# جایگزینی
new_text = text.replace("Hello", "Hi")
print("جایگزین:", new_text)

# پیدا کردن
print("ایندکس Network:", text.find("Network"))

# شمارش
print("تعداد e:", text.count("e"))

# تقسیم به لیست
words = text.split()
print("کلمات:", words)

# اتصال لیست به رشته
joined = "-".join(words)
print("اتصال:", joined)

# بررسی شروع و پایان
print("شروع با Hello:", text.startswith("Hello"))
print("پایان با !:", text.endswith("!"))

# ============================================
# بخش ۲: فرمت‌دهی رشته (f-string)
# ============================================

name = "Yasmin"
age = 20
print(f"اسم: {name}, سن: {age}")

# فرمت اعداد
pi = 3.14159
print(f"پی: {pi:.2f}")  # 2 رقم اعشار

# ============================================
# بخش ۳: Regex - جستجوی الگو
# ============================================

# --- پیدا کردن IP ---
log = "Connection from 192.168.1.100 failed"
ip_pattern = r'\d+\.\d+\.\d+\.\d+'
ip = re.search(ip_pattern, log)
print("\nIP پیدا شده:", ip.group())

# --- پیدا کردن همه‌ی IPها ---
logs = """
192.168.1.1 connected
10.0.0.5 disconnected
172.16.0.10 connected
"""
all_ips = re.findall(ip_pattern, logs)
print("همه IPها:", all_ips)

# --- پیدا کردن ایمیل ---
text_email = "Contact: admin@example.com or support@test.org"
email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
emails = re.findall(email_pattern, text_email)
print("ایمیل‌ها:", emails)

# --- پیدا کردن URL ---
text_url = "Visit https://github.com or http://example.com"
url_pattern = r'https?://[\w\.-]+'
urls = re.findall(url_pattern, text_url)
print("URLها:", urls)

# --- پیدا کردن تاریخ ---
text_date = "Log date: 2026-09-22"
date_pattern = r'\d{4}-\d{2}-\d{2}'
dates = re.findall(date_pattern, text_date)
print("تاریخ‌ها:", dates)

# --- جایگزینی با Regex ---
masked = re.sub(ip_pattern, "XXX.XXX.XXX.XXX", log)
print("IP مخفی شده:", masked)

# ============================================
# بخش ۴: اعتبارسنجی (Validation)
# ============================================

def is_valid_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return bool(re.match(pattern, ip))

print("\nاعتبارسنجی IP:")
print("192.168.1.1 →", is_valid_ip("192.168.1.1"))
print("999.999.999.999 →", is_valid_ip("999.999.999.999"))
print("abc →", is_valid_ip("abc"))

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

print("\nاعتبارسنجی ایمیل:")
print("user@example.com →", is_valid_email("user@example.com"))
print("invalid →", is_valid_email("invalid"))

# ============================================
# بخش ۵: پارس کردن لاگ شبکه (کاربردی!)
# ============================================

log_line = "2026-09-22 10:30:45 ERROR 192.168.1.50 Connection timeout"

pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) ([\d\.]+) (.+)'
match = re.match(pattern, log_line)

if match:
    date, time, level, ip, message = match.groups()
    print("\n=== تحلیل لاگ ===")
    print(f"تاریخ: {date}")
    print(f"ساعت: {time}")
    print(f"سطح: {level}")
    print(f"IP: {ip}")
    print(f"پیام: {message}")

# ============================================
# بخش ۶: تمرین‌های کاربردی
# ============================================

print("\n=== تمرین‌ها ===")

# تمرین ۱: استخراج تمام اعداد از یک متن
text_nums = "There are 42 apples and 17 oranges, total 59"
nums = re.findall(r'\d+', text_nums)
print("اعداد:", nums)

# تمرین ۲: پیدا کردن کلمات با حرف بزرگ
text_words = "Python is Great for Network Automation"
caps = re.findall(r'\b[A-Z]\w+', text_words)
print("کلمات با حرف بزرگ:", caps)

# تمرین ۳: پاک کردن کاراکترهای غیرضروری
messy = "Hello!!! @#$ World???"
clean = re.sub(r'[^\w\s]', '', messy)
print("پاک شده:", clean)

# تمرین ۴: جدا کردن نام و دامنه ایمیل
email = "yasmin@gmail.com"
parts = re.match(r'([\w\.-]+)@([\w\.-]+)', email)
print(f"نام کاربری: {parts.group(1)}")
print(f"دامنه: {parts.group(2)}")

# تمرین ۵: استخراج پورت از آدرس
address = "192.168.1.1:8080"
port_match = re.search(r':(\d+)$', address)
if port_match:
    print(f"پورت: {port_match.group(1)}")