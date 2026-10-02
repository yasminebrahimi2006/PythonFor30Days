import os
import sys

# ============================================
# بخش ۱: os - مسیر و فایل
# ============================================
print("=== os - مسیر ===")

print(f"مسیر فعلی: {os.getcwd()}")
print(f"سیستم‌عامل: {os.name}")

# لیست فایل‌ها
print("\nفایل‌های پوشه‌ی فعلی:")
for item in os.listdir("."):
    kind = "📁" if os.path.isdir(item) else "📄"
    print(f"  {kind} {item}")

# ============================================
# بخش ۲: os.path
# ============================================
print("\n=== os.path ===")

path = os.path.join("Week01", "Day01_lists.py")
print(f"مسیر: {path}")
print(f"نام فایل: {os.path.basename(path)}")
print(f"پوشه: {os.path.dirname(path)}")

# بررسی
print(f"\ntest.txt وجود داره؟ {os.path.exists('test.txt')}")
print(f"Week01 پوشه هست؟ {os.path.isdir('Week01')}")

# ============================================
# بخش ۳: متغیرهای محیطی
# ============================================
print("\n=== متغیرهای محیطی ===")

# خواندن
path_env = os.getenv("PATH", "")
print(f"PATH طول: {len(path_env)} کاراکتر")

# با پیش‌فرض
api_key = os.getenv("API_KEY", "not_set")
print(f"API_KEY: {api_key}")

# تنظیم
os.environ["MY_VAR"] = "hello"
print(f"MY_VAR: {os.getenv('MY_VAR')}")

# ============================================
# بخش ۴: sys - اطلاعات
# ============================================
print("\n=== sys ===")

print(f"نسخه پایتون: {sys.version.split()[0]}")
print(f"آرگومان‌ها: {sys.argv}")

# ============================================
# بخش ۵: os.walk (پیمایش تودرتو)
# ============================================
print("\n=== os.walk ===")

for root, dirs, files in os.walk("."):
    # فقط پوشه‌های سطح اول
    level = root.count(os.sep)
    if level > 2:
        continue
    
    indent = "  " * level
    print(f"{indent}{root}/")
    for file in files[:3]:   # فقط ۳ تا اول
        print(f"{indent}  - {file}")

# ============================================
# بخش ۶: ابزار خط فرمان
# ============================================
print("\n=== ابزار خط فرمان ===")

def show_info():
    print(f"مسیر: {os.getcwd()}")
    print(f"پایتون: {sys.version.split()[0]}")
    print(f"سیستم: {os.name}")

def list_files():
    for item in os.listdir("."):
        print(f"  {item}")

if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == "info":
        show_info()
    elif command == "list":
        list_files()
    else:
        print(f"دستور ناشناخته: {command}")
else:
    print("(برای تست: python Day12_os_sys.py info)")
    print("(یا: python Day12_os_sys.py list)")

# ============================================
# بخش ۷: اسکن پوشه
# ============================================
print("\n=== اسکن پوشه ===")

def scan_python_files(folder):
    files = []
    for root, dirs, filenames in os.walk(folder):
        for file in filenames:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                size = os.path.getsize(full_path)
                files.append((full_path, size))
    return files

python_files = scan_python_files("Week01")
print(f"تعداد فایل‌های پایتون: {len(python_files)}")
for path, size in python_files[:5]:
    print(f"  {path} ({size} bytes)")

# ============================================
# بخش ۸: تنظیمات از محیط
# ============================================
print("\n=== تنظیمات ===")

def get_config():
    return {
        "api_key": os.getenv("API_KEY", "not_set"),
        "base_url": os.getenv("BASE_URL", "https://api.example.com"),
        "debug": os.getenv("DEBUG", "false").lower() == "true"
    }

config = get_config()
print(f"API Key: {config['api_key']}")
print(f"Base URL: {config['base_url']}")
print(f"Debug: {config['debug']}")

# ============================================
# بخش ۹: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱
print(f"۱. مسیر: {os.getcwd()}")
print(f"   سیستم: {os.name}")

# تمرین ۲
py_files = [f for f in os.listdir(".") if f.endswith(".py")]
print(f"۲. فایل‌های پایتون: {py_files}")

# تمرین ۳
def check_file(filename):
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        return f"{filename} ({size} bytes)"
    return f"{filename} پیدا نشد"

print(f"۳. test.txt: {check_file('test.txt')}")
print(f"   nonexistent.txt: {check_file('nonexistent.txt')}")

# تمرین ۴
if len(sys.argv) > 1:
    print(f"۴. آرگومان: {sys.argv[1]}")
else:
    print("۴. آرگومانی وارد نشد")

# تمرین ۵
print(f"۵. API Key: {os.getenv('API_KEY', 'not_set')}")