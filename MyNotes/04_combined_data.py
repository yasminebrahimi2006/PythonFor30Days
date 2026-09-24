import json

# ============================================
# بخش ۱: لیست دیکشنری‌ها
# ============================================
print("=== لیست دیکشنری‌ها ===")

students = [
    {"name": "Ali", "age": 20, "grades": [18, 17, 19]},
    {"name": "Sara", "age": 22, "grades": [20, 19, 18]},
    {"name": "Reza", "age": 21, "grades": [15, 16, 14]},
]

for student in students:
    avg = sum(student["grades"]) / len(student["grades"])
    print(f"  {student['name']} ({student['age']}) - معدل: {avg:.2f}")

# ============================================
# بخش ۲: دیکشنری با مقادیر لیست
# ============================================
print("\n=== دیکشنری با لیست ===")

classes = {
    "math": ["Ali", "Sara", "Reza"],
    "physics": ["Sara", "Reza"],
    "chemistry": ["Ali", "Sara"]
}

for subject, students_list in classes.items():
    print(f"  {subject}: {len(students_list)} دانش‌آموز")

# ============================================
# بخش ۳: دیکشنری تودرتو
# ============================================
print("\n=== دیکشنری تودرتو ===")

company = {
    "dev": {
        "lead": {"name": "Ali", "age": 30},
        "junior": {"name": "Sara", "age": 22}
    },
    "design": {
        "lead": {"name": "Reza", "age": 28}
    }
}

for dept, roles in company.items():
    print(f"\n  {dept}:")
    for role, info in roles.items():
        print(f"    {role}: {info['name']} ({info['age']})")

# ============================================
# بخش ۴: لیست تاپل‌ها
# ============================================
print("\n=== لیست تاپل‌ها ===")

servers = [
    ("server1", "192.168.1.1", 8080),
    ("server2", "192.168.1.2", 8081),
    ("server3", "192.168.1.3", 8082),
]

for name, ip, port in servers:
    print(f"  {name}: {ip}:{port}")

# ============================================
# بخش ۵: عملیات روی داده‌های ترکیبی
# ============================================
print("\n=== عملیات ===")

products = [
    {"name": "Laptop", "price": 1500, "stock": 5},
    {"name": "Phone", "price": 800, "stock": 0},
    {"name": "Tablet", "price": 600, "stock": 10},
]

# فیلتر
available = [p for p in products if p["stock"] > 0]
print("موجود:", [p["name"] for p in available])

# مرتب‌سازی
sorted_by_price = sorted(products, key=lambda p: p["price"])
print("مرتب بر اساس قیمت:", [p["name"] for p in sorted_by_price])

# گرون‌ترین
most_expensive = max(products, key=lambda p: p["price"])
print(f"گرون‌ترین: {most_expensive['name']}")

# جمع
total = sum(p["price"] for p in products)
print(f"جمع قیمت‌ها: {total}")

# ============================================
# بخش ۶: تبدیل ساختارها
# ============================================
print("\n=== تبدیل ===")

students_list = [
    {"id": "s1", "name": "Ali", "age": 20},
    {"id": "s2", "name": "Sara", "age": 22},
    {"id": "s3", "name": "Reza", "age": 21},
]

by_id = {s["id"]: s for s in students_list}
print("دیکشنری با id:", by_id.keys())
print("دسترسی به s2:", by_id["s2"]["name"])

# ============================================
# بخش ۷: JSON
# ============================================
print("\n=== JSON ===")

data = {
    "users": [
        {"id": 1, "name": "Ali", "skills": ["Python", "Network"]},
        {"id": 2, "name": "Sara", "skills": ["Design", "UI"]},
    ],
    "total": 2
}

json_str = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str)

# ============================================
# بخش ۸: گروه‌بندی
# ============================================
print("\n=== گروه‌بندی ===")

logs = [
    {"level": "INFO", "message": "Server started"},
    {"level": "ERROR", "message": "Connection failed"},
    {"level": "INFO", "message": "User logged in"},
    {"level": "ERROR", "message": "Timeout"},
]

grouped = {}
for log in logs:
    level = log["level"]
    grouped.setdefault(level, []).append(log["message"])

for level, messages in grouped.items():
    print(f"  {level}: {len(messages)} پیام")

# ============================================
# بخش ۹: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱: میانگین
students = [
    {"name": "Ali", "grades": [18, 17, 19]},
    {"name": "Sara", "grades": [20, 19, 18]},
    {"name": "Reza", "grades": [15, 16, 14]},
]
print("\n۱. میانگین نمرات:")
for s in students:
    avg = sum(s["grades"]) / len(s["grades"])
    print(f"   {s['name']}: {avg:.2f}")

# تمرین ۲: گرون‌ترین
products = [
    {"name": "Laptop", "price": 1500},
    {"name": "Phone", "price": 800},
    {"name": "Tablet", "price": 600},
]
most_expensive = max(products, key=lambda p: p["price"])
print(f"\n۲. گرون‌ترین: {most_expensive['name']} - {most_expensive['price']}")

# تمرین ۳: گروه‌بندی
people = [
    {"name": "Ali", "city": "Tehran"},
    {"name": "Sara", "city": "Shiraz"},
    {"name": "Reza", "city": "Tehran"},
    {"name": "Maryam", "city": "Shiraz"},
]
by_city = {}
for p in people:
    by_city.setdefault(p["city"], []).append(p["name"])
print(f"\n۳. گروه‌بندی: {by_city}")

# تمرین ۴: فیلتر
users = [
    {"name": "Ali", "active": True},
    {"name": "Sara", "active": False},
    {"name": "Reza", "active": True},
]
active_users = [u["name"] for u in users if u["active"]]
print(f"\n۴. کاربران فعال: {active_users}")

# تمرین ۵: سبد خرید
cart = [
    {"item": "Book", "price": 50, "quantity": 2},
    {"item": "Pen", "price": 5, "quantity": 10},
    {"item": "Bag", "price": 100, "quantity": 1},
]
total = sum(item["price"] * item["quantity"] for item in cart)
print(f"\n۵. جمع سبد خرید: {total}")