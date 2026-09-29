from datetime import datetime, date, time, timedelta, timezone
import time

# ============================================
# بخش ۱: تاریخ و زمان فعلی
# ============================================
print("=== تاریخ و زمان فعلی ===")

now = datetime.now()
print(f"الان: {now}")
print(f"امروز: {date.today()}")
print(f"UTC: {datetime.utcnow()}")

# ============================================
# بخش ۲: دسترسی به اجزا
# ============================================
print("\n=== اجزا ===")
print(f"سال: {now.year}")
print(f"ماه: {now.month}")
print(f"روز: {now.day}")
print(f"ساعت: {now.hour}")
print(f"دقیقه: {now.minute}")
print(f"روز هفته: {now.weekday()}")

# ============================================
# بخش ۳: فرمت‌دهی
# ============================================
print("\n=== فرمت‌دهی ===")
print(now.strftime("%Y-%m-%d"))
print(now.strftime("%Y/%m/%d %H:%M:%S"))
print(now.strftime("%A, %d %B %Y"))
print(now.strftime("%I:%M %p"))   # 12-hour

# ============================================
# بخش ۴: پارس کردن
# ============================================
print("\n=== پارس کردن ===")

date_str = "2026-09-29 14:30:45"
parsed = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print(f"پارس شده: {parsed}")
print(f"نوع: {type(parsed)}")

# ============================================
# بخش ۵: timedelta
# ============================================
print("\n=== timedelta ===")

print(f"فردا: {(now + timedelta(days=1)).strftime('%Y-%m-%d')}")
print(f"دیروز: {(now - timedelta(days=1)).strftime('%Y-%m-%d')}")
print(f"هفته بعد: {(now + timedelta(weeks=1)).strftime('%Y-%m-%d')}")
print(f"۲ ساعت بعد: {(now + timedelta(hours=2)).strftime('%H:%M')}")

# ============================================
# بخش ۶: اختلاف
# ============================================
print("\n=== اختلاف ===")

start = datetime(2026, 1, 1)
end = datetime(2026, 12, 31)
diff = end - start
print(f"اختلاف: {diff.days} روز")
print(f"ثانیه: {diff.total_seconds()}")

# محاسبه سن
birth = datetime(2006, 5, 15)
age_days = (now - birth).days
print(f"سن: {age_days // 365} سال و {age_days % 365} روز")

# ============================================
# بخش ۷: مقایسه
# ============================================
print("\n=== مقایسه ===")
d1 = datetime(2026, 1, 1)
d2 = datetime(2026, 12, 31)
print(f"d1 < d2: {d1 < d2}")
print(f"d1 > d2: {d1 > d2}")

# ============================================
# بخش ۸: Timezone
# ============================================
print("\n=== Timezone ===")

utc_now = datetime.now(timezone.utc)
tehran_tz = timezone(timedelta(hours=3, minutes=30))
tehran_now = datetime.now(tehran_tz)
print(f"UTC: {utc_now.strftime('%H:%M')}")
print(f"Tehran: {tehran_now.strftime('%H:%M')}")

# ============================================
# بخش ۹: Timestamp
# ============================================
print("\n=== Timestamp ===")

ts = now.timestamp()
print(f"Timestamp: {ts:.0f}")
print(f"از timestamp: {datetime.fromtimestamp(ts)}")

# ============================================
# بخش ۱۰: تحلیل لاگ شبکه
# ============================================
print("\n=== تحلیل لاگ ===")

logs = [
    "2026-09-29 10:00:00 INFO Server started",
    "2026-09-29 10:05:30 ERROR Connection failed",
    "2026-09-29 10:10:15 WARNING High memory",
]

for log in logs:
    dt = datetime.strptime(log[:19], "%Y-%m-%d %H:%M:%S")
    level = log.split()[2]
    message = " ".join(log.split()[3:])
    print(f"  [{dt.strftime('%H:%M')}] {level}: {message}")

# ============================================
# بخش ۱۱: Token با انقضا
# ============================================
print("\n=== Token ===")

class Token:
    def __init__(self, value, expires_in_hours=24):
        self.value = value
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(hours=expires_in_hours)
    
    def is_expired(self):
        return datetime.now() > self.expires_at
    
    def __str__(self):
        return f"Token: {self.value[:8]}... | انقضا: {self.expires_at.strftime('%H:%M')}"

token = Token("abc123xyz456", expires_in_hours=2)
print(token)
print(f"منقضی شده؟ {token.is_expired()}")

# ============================================
# بخش ۱۲: تایمر
# ============================================
print("\n=== تایمر ===")

start_time = datetime.now()
time.sleep(0.5)   # شبیه‌سازی کار
end_time = datetime.now()

duration = end_time - start_time
print(f"مدت: {duration.total_seconds():.2f} ثانیه")

# ============================================
# بخش ۱۳: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱
print(f"۱. امروز: {now.strftime('%Y-%m-%d')} - {now.strftime('%A')}")

# تمرین ۲
age_days = (now - datetime(2006, 5, 15)).days
print(f"۲. سن: {age_days // 365} سال")

# تمرین ۳
print("۳. تاریخ‌های آینده:")
for days in [1, 7, 30]:
    future = now + timedelta(days=days)
    print(f"   {days} روز بعد: {future.strftime('%Y-%m-%d')}")

# تمرین ۴
print("۴. لاگ‌ها:")
for log in logs:
    dt = datetime.strptime(log[:19], "%Y-%m-%d %H:%M:%S")
    print(f"   {dt.strftime('%H:%M:%S')}")

# تمرین ۵
start = datetime.now()
time.sleep(0.1)
print(f"۵. مدت: {(datetime.now() - start).total_seconds():.3f} ثانیه")