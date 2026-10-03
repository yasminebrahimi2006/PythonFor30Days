import subprocess
import platform
import re

# ============================================
# بخش ۱: دستور ساده
# ============================================
print("=== دستور ساده ===")

result = subprocess.run(
    ["echo", "Hello from subprocess!"],
    capture_output=True,
    text=True
)
print(f"خروجی: {result.stdout.strip()}")
print(f"کد خروج: {result.returncode}")

# ============================================
# بخش ۲: اطلاعات سیستم
# ============================================
print("\n=== اطلاعات سیستم ===")

if platform.system().lower() == "windows":
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
else:
    result = subprocess.run(["ifconfig"], capture_output=True, text=True)

# چاپ ۵ خط اول
for line in result.stdout.split("\n")[:5]:
    print(f"  {line}")

# ============================================
# بخش ۳: پینگ
# ============================================
print("\n=== پینگ ===")

def ping(host, count=1, timeout=5):
    """پینگ یه هاست"""
    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout
    except subprocess.TimeoutExpired:
        return False, "Timeout!"

success, output = ping("8.8.8.8")
print(f"8.8.8.8: {'✅ موفق' if success else '❌ ناموفق'}")
print(f"خروجی:\n{output[:200]}...")

# ============================================
# بخش ۴: مدیریت خطا
# ============================================
print("\n=== مدیریت خطا ===")

try:
    result = subprocess.run(
        ["ping", "-n", "1", "nonexistent-host-xyz.com"],
        capture_output=True,
        text=True,
        timeout=10,
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"خطا: returncode={e.returncode}")
except subprocess.TimeoutExpired:
    print("Timeout!")

# ============================================
# بخش ۵: پینگ چند سرور
# ============================================
print("\n=== پینگ چند سرور ===")

servers = ["8.8.8.8", "1.1.1.1", "192.168.1.1"]

for server in servers:
    success, _ = ping(server)
    status = "✅ آنلاین" if success else "❌ آفلاین"
    print(f"  {server}: {status}")

# ============================================
# بخش ۶: لیست پورت‌های باز
# ============================================
print("\n=== پورت‌های باز ===")

def get_open_ports():
    result = subprocess.run(
        ["netstat", "-an"],
        capture_output=True,
        text=True
    )
    
    ports = set()
    for line in result.stdout.split("\n"):
        if "LISTENING" in line or "LISTEN" in line:
            match = re.search(r':(\d+)\s', line)
            if match:
                ports.add(int(match.group(1)))
    
    return sorted(ports)

open_ports = get_open_ports()
print(f"تعداد پورت‌های باز: {len(open_ports)}")
for port in open_ports[:10]:
    print(f"  {port}")

# ============================================
# بخش ۷: nslookup
# ============================================
print("\n=== nslookup ===")

result = subprocess.run(
    ["nslookup", "google.com"],
    capture_output=True,
    text=True,
    timeout=10
)

for line in result.stdout.split("\n"):
    if "Address" in line:
        print(f"  {line.strip()}")

# ============================================
# بخش ۸: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱
r = subprocess.run(["echo", "test"], capture_output=True, text=True)
print(f"۱. {r.stdout.strip()}")

# تمرین ۲
success, _ = ping("8.8.8.8")
print(f"۲. 8.8.8.8: {'✅' if success else '❌'}")

# تمرین ۳
if platform.system().lower() == "windows":
    r = subprocess.run(["ipconfig"], capture_output=True, text=True)
    for line in r.stdout.split("\n"):
        if "IPv4" in line:
            print(f"۳. {line.strip()}")

# تمرین ۴
ports = get_open_ports()
print(f"۴. پورت‌ها: {ports[:5]}")

# تمرین ۵
print("۵. پینگ سرورها:")
for server in ["8.8.8.8", "1.1.1.1"]:
    ok, _ = ping(server, timeout=3)
    print(f"   {server}: {'✅' if ok else '❌'}")