#  JSON Cheat Sheet

---

##  انواع داده در JSON

| نوع | مثال | توضیح |
|-----|------|-------|
| **String** | `"Yasmin"` | همیشه داخل `"` |
| **Number** | `20` ، `3.14` ، `-5` | صحیح یا اعشاری |
| **Boolean** | `true` ، `false` | **حروف کوچک** |
| **null** | `null` | خالی / هیچ |
| **Object** | `{ "key": "value" }` | معادل `dict` |
| **Array** | `[1, 2, 3]` | معادل `list` |

---


###  قوانین طلایی:
1. **کلیدها همیشه در `"` دوتایی** — نه تک
2. **آخرین آیتم نباید کاما داشته باشد**
3. **کاما بین آیتم‌ها** — نه بعد از آخرین
4. `true` / `false` / `null` → **حروف کوچک**
5. کامنت (`//` یا `#`) **مجاز نیست**

---

##  JSON در پایتون — ۴ تابع مهم

```python
import json
```

| تابع | ورودی | خروجی | کاربرد |
|------|-------|-------|--------|
| `json.dumps(obj)` | dict | str | تبدیل به **رشته** |
| `json.loads(str)` | str | dict | تبدیل از **رشته** |
| `json.dump(obj, file)` | dict + file | — | نوشتن در **فایل** |
| `json.load(file)` | file | dict | خواندن از **فایل** |

---

##  مثال‌های کاربردی

### 1 dict → رشته (dumps)

```python
import json

data = {"name": "Yasmin", "age": 20}
text = json.dumps(data)
print(text)          # '{"name": "Yasmin", "age": 20}'
print(type(text))    # <class 'str'>
```

### 2️ رشته → dict (loads)

```python
text = '{"name": "Yasmin", "age": 20}'
data = json.loads(text)
print(data["name"])  # Yasmin
print(type(data))    # <class 'dict'>
```

### 3️ نوشتن در فایل (dump)

```python
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
```

### 4️ خواندن از فایل (load)

```python
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded["name"])
```

---

##  پارامترهای مهم

| پارامتر | مقادیر | کار |
|---------|--------|-----|
| `indent` | `2` / `4` / `None` | فاصله‌گذاری خوانا |
| `ensure_ascii` | `True` / `False` | نمایش فارسی |
| `sort_keys` | `True` / `False` | مرتب کردن کلیدها |
| `separators` | `(",", ":")` | جداکننده‌ها |

---

##  تبدیل پایتون ↔ JSON

| پایتون | JSON |
|--------|------|
| `dict` | object `{}` |
| `list` ، `tuple` | array `[]` |
| `str` | string |
| `int` ، `float` | number |
| `True` | `true` |
| `False` | `false` |
| `None` | `null` |

---

##  ساختارهای تودرتو (Nested)

```json
{
    "user": {
        "name": "Yasmin",
        "contact": {
            "email": "y@example.com",
            "phone": "0912..."
        }
    },
    "skills": [
        {"name": "Python", "level": 5},
        {"name": "Network", "level": 4}
    ]
}
```

### دسترسی در پایتون:

```python
data["user"]["contact"]["email"]        # y@example.com
data["skills"][0]["name"]                # Python
data["skills"][1]["level"]               # 4
```

---

##  خطاهای رایج

| خطا | علت | راه‌حل |
|-----|-----|--------|
| `JSONDecodeError` | JSON نامعتبر | ساختار را چک کن |
| `TypeError` | نوع داده غیرمجاز | به رشته/عدد تبدیل کن |
| `KeyError` | کلید وجود ندارد | از `.get()` استفاده کن |
| `UnicodeDecodeError` | انکودینگ اشتباه | `encoding="utf-8"` |

### نمونه مدیریت خطا:

```python
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("فایل نیست!")
except json.JSONDecodeError as e:
    print(f"JSON خرابه: {e}")
```

---

##  دسترسی امن به داده

```python
data = {"name": "Yasmin", "age": 20}

#  خطرناک
data["city"]              # KeyError!

#  امن
data.get("city")          # None
data.get("city", "N/A")   # "N/A"
```

---

##  نمونه فایل کامل

**`config.json`**
```json
{
    "app_name": "MyApp",
    "version": "1.0.0",
    "debug": true,
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "users": [
        {"id": 1, "name": "Yasmin", "admin": true},
        {"id": 2, "name": "Ali", "admin": false}
    ],
    "timeout": null
}
```

**خواندن در پایتون:**
```python
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["app_name"])                  # MyApp
print(config["database"]["port"])          # 5432
print(config["users"][0]["name"])          # Yasmin
print(config["debug"])                     # True
```

---

##  JSON در API

```python
import requests

# ارسال JSON
response = requests.post(
    "https://api.example.com/user",
    json={"name": "Yasmin", "age": 20}     # ← json= خودکار تبدیل می‌کند
)

# دریافت JSON
data = response.json()                     # ← خودکار تبدیل به dict
print(data["status"])
```

**نکته:** با `requests` نیازی به `json.dumps()` دستی نیست.

---

##  ابزارهای کاربردی

| ابزار | کار |
|-------|-----|
| [jsonlint.com](https://jsonlint.com) | اعتبارسنجی JSON |
| `python -m json.tool file.json` | فرمت‌دهی در ترمینال |
| `jq` (Linux/Mac) | پردازش JSON در خط فرمان |
| VS Code | نمایش درختی JSON |

---

##  نکات طلایی

1. **همیشه `encoding="utf-8"`** در `open()`
2. **همیشه `ensure_ascii=False`** برای فارسی
3. **همیشه `indent=4`** برای خوانایی
4. **همیشه `try/except`** برای خواندن فایل
5. **از `.get()`** برای دسترسی امن
6. **`dumps`/`loads`** → رشته | **`dump`/`load`** → فایل
7. **JSON کامنت ندارد** — از فیلد `"_comment"` استفاده کن
8. **عدد بزرگ یا اعشاری دقیق** → JSON محدودیت دارد

---

##  الگوی آماده (Template)

```python
import json
from pathlib import Path

def save_json(data, filename):
    """ذخیره داده در فایل JSON"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_json(filename, default=None):
    """خواندن امن JSON"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError as e:
        print(f"خطای JSON: {e}")
        return default

# استفاده
save_json({"name": "Yasmin"}, "user.json")
user = load_json("user.json", default={})
print(user.get("name"))
```

---

