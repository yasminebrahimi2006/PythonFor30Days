import json
import logging

# ============ بخش ۱: نوشتن فایل ============
with open("test.txt", "w", encoding="utf-8") as file:
    file.write("سلام دنیا!\n")
    file.write("این یه فایل تستیه.\n")
print("فایل نوشته شد.")

# ============ بخش ۲: خواندن فایل ============
with open("test.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print("محتوای فایل:")
    print(content)

# ============ بخش ۳: خواندن خط به خط ============
print("خط به خط:")
with open("test.txt", "r", encoding="utf-8") as file:
    for line in file:
        print("  -", line.strip())

# ============ بخش ۴: اضافه کردن ============
with open("test.txt", "a", encoding="utf-8") as file:
    file.write("خط جدید.\n")
print("خط جدید اضافه شد.")

# ============ بخش ۵: try/except ============
print("\n=== مدیریت خطا ===")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "تقسیم بر صفر!"
    except TypeError:
        return "ورودی باید عدد باشه!"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("a", 2))

# ============ بخش ۶: خواندن فایل با خطا ============
def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"فایل {filename} پیدا نشد!")
        return None
    except Exception as e:
        print(f"خطا: {e}")
        return None

content = read_file("test.txt")
if content:
    print("فایل با موفقیت خونده شد.")

# ============ بخش ۷: JSON ============
print("\n=== JSON ===")

data = {
    "name": "Yasmin",
    "age": 20,
    "skills": ["Python", "Network", "API"]
}

# نوشتن
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
print("JSON نوشته شد.")

# خواندن
with open("data.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)
    print("نام:", loaded["name"])
    print("مهارت‌ها:", loaded["skills"])

# ============ بخش ۸: Logging ============
print("\n=== Logging ===")

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("برنامه شروع شد")
logging.warning("این یه هشداره")
logging.error("این یه خطاست")
print("لاگ‌ها توی app.log ذخیره شدند.")

# ============ تمرین‌ها ============
print("\n=== تمرین‌ها ===")

# تمرین ۱: ذخیره لیست
numbers = [10, 20, 30, 40, 50]
with open("numbers.txt", "w") as file:
    for num in numbers:
        file.write(f"{num}\n")

with open("numbers.txt", "r") as file:
    loaded = [int(line.strip()) for line in file]
    print("لیست خونده شده:", loaded)

# تمرین ۲: شمارش خطوط
def count_lines(filename):
    try:
        with open(filename, "r") as file:
            return len(file.readlines())
    except FileNotFoundError:
        return 0

print("تعداد خطوط test.txt:", count_lines("test.txt"))

# تمرین ۳: تحلیل لاگ
def analyze_log(filename):
    errors = 0
    try:
        with open(filename, "r") as file:
            for line in file:
                if "ERROR" in line:
                    errors += 1
    except FileNotFoundError:
        print("فایل پیدا نشد!")
        return
    print(f"تعداد خطاها: {errors}")

analyze_log("app.log")