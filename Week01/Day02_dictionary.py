# ساختن دیکشنری
person = {
    "name": "Yasmin",
    "age": 20,
    "city": "Tehran"
}

# دسترسی
print(person["name"])
print(person.get("age"))
print(person.get("job", "Unknown"))   # مقدار پیش‌فرض

# اضافه/تغییر
person["job"] = "Developer"
person["age"] = 21

# حذف
del person["city"]
person.pop("job")

# حلقه
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(f"{key}: {value}")

# کلیدها و مقادیر
print(person.keys())
print(person.values())