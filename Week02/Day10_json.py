import json
from datetime import datetime

# ============================================
# بخش ۱: تبدیل پایتون به JSON
# ============================================
print("=== پایتون به JSON ===")

data = {
    "name": "Yasmin",
    "age": 20,
    "skills": ["Python", "Network"],
    "is_student": True,
    "address": None
}

json_str = json.dumps(data, indent=4, ensure_ascii=False)
print(json_str)

# ============================================
# بخش ۲: تبدیل JSON به پایتون
# ============================================
print("\n=== JSON به پایتون ===")

json_str2 = '{"name": "Ali", "age": 25, "skills": ["Python", "Java"]}'
parsed = json.loads(json_str2)

print(f"نوع: {type(parsed)}")
print(f"نام: {parsed['name']}")
print(f"مهارت‌ها: {parsed['skills']}")

# ============================================
# بخش ۳: نوشتن توی فایل
# ============================================
print("\n=== نوشتن فایل ===")

users = [
    {"id": 1, "name": "Ali", "age": 25},
    {"id": 2, "name": "Sara", "age": 22},
    {"id": 3, "name": "Reza", "age": 28}
]

with open("users.json", "w", encoding="utf-8") as file:
    json.dump(users, file, indent=2, ensure_ascii=False)

print("فایل users.json ذخیره شد.")

# ============================================
# بخش ۴: خواندن از فایل
# ============================================
print("\n=== خواندن فایل ===")

with open("users.json", "r", encoding="utf-8") as file:
    loaded_users = json.load(file)

for user in loaded_users:
    print(f"  {user['id']}: {user['name']} ({user['age']})")

# ============================================
# بخش ۵: پاسخ API
# ============================================
print("\n=== پاسخ API ===")

api_response = '''
{
    "status": "success",
    "data": {
        "user": {
            "id": 1,
            "name": "Yasmin",
            "email": "yasmin@example.com"
        },
        "posts": [
            {"id": 1, "title": "First Post"},
            {"id": 2, "title": "Second Post"}
        ]
    }
}
'''

response = json.loads(api_response)
print(f"وضعیت: {response['status']}")
print(f"نام: {response['data']['user']['name']}")
print(f"تعداد پست‌ها: {len(response['data']['posts'])}")

for post in response["data"]["posts"]:
    print(f"  - {post['title']}")

# ============================================
# بخش ۶: JSON تودرتو
# ============================================
print("\n=== JSON تودرتو ===")

company = {
    "name": "TechCorp",
    "employees": [
        {"name": "Ali", "position": "Developer", "skills": ["Python", "Django"]},
        {"name": "Sara", "position": "Designer", "skills": ["Figma", "Photoshop"]}
    ]
}

print(json.dumps(company, indent=2, ensure_ascii=False))

# ============================================
# بخش ۷: مدیریت خطا
# ============================================
print("\n=== مدیریت خطا ===")

bad_json = '{"name": "Yasmin", "age":}'

try:
    data = json.loads(bad_json)
except json.JSONDecodeError as e:
    print(f"خطای JSON: {e}")

# ============================================
# بخش ۸: datetime در JSON
# ============================================
print("\n=== datetime ===")

data = {
    "name": "Yasmin",
    "created_at": datetime.now().isoformat()
}
print(json.dumps(data, indent=2))

# ============================================
# بخش ۹: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱: دیکشنری به JSON
person = {"name": "Yasmin", "age": 20, "skills": ["Python", "Network"]}
print("۱.", json.dumps(person, ensure_ascii=False))

# تمرین ۲: JSON به دیکشنری
json_str = '{"name": "Ali", "age": 25}'
print(f"۲. {json.loads(json_str)['name']}")

# تمرین ۳: ذخیره و خواندن
with open("users.json", "w", encoding="utf-8") as f:
    json.dump(users, f, indent=2, ensure_ascii=False)
with open("users.json", "r", encoding="utf-8") as f:
    print(f"۳. تعداد کاربران: {len(json.load(f))}")

# تمرین ۴: پاسخ API
response = '{"status": "ok", "data": {"temperature": 25, "city": "Tehran"}}'
data = json.loads(response)
print(f"۴. {data['data']['city']}: {data['data']['temperature']}°C")

# تمرین ۵: ساخت payload
new_user = {
    "username": "yasmin",
    "email": "yasmin@example.com",
    "profile": {"age": 20, "city": "Tehran"}
}
print(f"۵. {json.dumps(new_user, ensure_ascii=False)}")