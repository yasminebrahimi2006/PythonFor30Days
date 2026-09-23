#   Creating a Dictionary   =============================================
# دیکشنری خالی
my_dict = {}

# دیکشنری ساده
person = {
    "name": "Yasmin",
    "age": 20,
    "city": "Tehran"
}

# با تابع dict()
person2 = dict(name="Ali", age=25, city="Shiraz")

# دیکشنری تودرتو
students = {
    "s1": {"name": "Ali", "age": 20},
    "s2": {"name": "Sara", "age": 22}
}



#   Accessing Values   =============================================
person = {"name": "Yasmin", "age": 20, "city": "Tehran"}

# روش ۱: با کروشه
print(person["name"])    # Yasmin

# روش ۲: با get (امن‌تر)
print(person.get("age"))         # 20
print(person.get("job"))         # None (چون وجود نداره)
print(person.get("job", "N/A"))  # N/A (مقدار پیش‌فرض)

#  تفاوت مهم:
# person["job"]  →  خطا میده (KeyError)
# person.get("job")  →  None برمی‌گردونه (بدون خطا)



#   Adding and Modifying   =============================================
person = {"name": "Yasmin", "age": 20}

# اضافه کردن
person["city"] = "Tehran"
person["job"] = "Developer"

# تغییر
person["age"] = 21

print(person)
# {'name': 'Yasmin', 'age': 21, 'city': 'Tehran', 'job': 'Developer'}

# اضافه کردن چند تا با هم
person.update({"country": "Iran", "language": "Persian"})



#   Deleting Items   =============================================
person = {"name": "Yasmin", "age": 20, "city": "Tehran", "job": "Dev"}

# روش ۱: با del
del person["job"]

# روش ۲: با pop (مقدار رو برمی‌گردونه)
city = person.pop("city")
print(city)  # Tehran

# روش ۳: با popitem (آخرین آیتم رو حذف می‌کنه)
last = person.popitem()

# روش ۴: پاک کردن همه
person.clear()

print(person)  # {}



#   Looping Through a Dictionary   =============================================
person = {"name": "Yasmin", "age": 20, "city": "Tehran"}

# فقط کلیدها
for key in person:
    print(key)

# فقط مقادیر
for value in person.values():
    print(value)

# کلید و مقدار با هم (بهترین روش)
for key, value in person.items():
    print(f"{key}: {value}")



#   Important Methods   =============================================
person = {"name": "Yasmin", "age": 20, "city": "Tehran"}

# کلیدها
print(person.keys())      # dict_keys(['name', 'age', 'city'])

# مقادیر
print(person.values())    # dict_values(['Yasmin', 20, 'Tehran'])

# آیتم‌ها
print(person.items())     # dict_items([('name', 'Yasmin'), ...])

# بررسی وجود کلید
print("name" in person)   # True
print("job" in person)    # False

# تعداد
print(len(person))        # 3

# کپی
person2 = person.copy()



#   Nested Dictionary   =============================================
students = {
    "s1": {"name": "Ali", "age": 20, "grades": [18, 17, 19]},
    "s2": {"name": "Sara", "age": 22, "grades": [20, 19, 18]},
    "s3": {"name": "Reza", "age": 21, "grades": [15, 16, 14]}
}

# دسترسی به داده‌های تودرتو
print(students["s1"]["name"])         # Ali
print(students["s2"]["grades"][0])    # 20

# حلقه روی همه
for id, info in students.items():
    print(f"{id}: {info['name']}, {info['age']} ساله")



#   Dictionary Comprehension   =============================================
    # روش معمولی
squares = {}
for i in range(1, 6):
    squares[i] = i ** 2

# روش کامپرهنشن
squares = {i: i ** 2 for i in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# با شرط
evens = {i: i ** 2 for i in range(1, 11) if i % 2 == 0}
print(evens)  # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}



#   Combining with Lists   =============================================
# لیستی از دیکشنری‌ها
products = [
    {"name": "Laptop", "price": 1500},
    {"name": "Phone", "price": 800},
    {"name": "Tablet", "price": 600}
]

# گرون‌ترین محصول
most_expensive = max(products, key=lambda p: p["price"])
print(most_expensive)  # {'name': 'Laptop', 'price': 1500}

# جمع قیمت‌ها
total = sum(p["price"] for p in products)
print(f"جمع کل: {total}")

# فیلتر کردن
cheap = [p for p in products if p["price"] < 1000]
print(cheap)



# ============ Exercises ============
print("\n=== Exercises ===")

# Exercise 1: Books
books = {
    "1984": "George Orwell",
    "Dune": "Frank Herbert",
    "Foundation": "Isaac Asimov"
}
print("\nBooks:")
for title, author in books.items():
    print(f"  {title} → {author}")

# Exercise 2: Average
grades = {"math": 18, "physics": 17, "chemistry": 19, "english": 20}
print(f"\nGrades average: {sum(grades.values())/len(grades):.2f}")

# Exercise 3: Word Count
text = "apple banana apple cherry banana apple"
word_count = {}
for word in text.split():
    word_count[word] = word_count.get(word, 0) + 1
print(f"\nWord count: {word_count}")

# Exercise 4: Merge
d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
print(f"\nMerge: {d1 | d2}")

# Exercise 5: Dictionary Comprehension
squares = {i: i**2 for i in range(1, 6)}
print(f"\nSquares: {squares}")
