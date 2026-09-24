# ============================================
# بخش ۱: تاپل (Tuple)
# ============================================
print("=== TUPLES ===")

# ساختن تاپل
coordinates = (10, 20)
colors = ("red", "green", "blue", "yellow")
single = (5,)

print("مختصات:", coordinates)
print("رنگ‌ها:", colors)
print("تک‌عضوی:", single)

# دسترسی
print("\nدسترسی:")
print("اولین رنگ:", colors[0])
print("آخرین رنگ:", colors[-1])
print("دو رنگ اول:", colors[:2])

# عملیات
numbers = (3, 1, 4, 1, 5, 9, 2, 6)
print("\nعملیات:")
print("طول:", len(numbers))
print("جمع:", sum(numbers))
print("بزرگ‌ترین:", max(numbers))
print("کوچک‌ترین:", min(numbers))
print("تعداد ۱:", numbers.count(1))
print("ایندکس ۵:", numbers.index(5))

# Unpacking
print("\nUnpacking:")
x, y = coordinates
print(f"x={x}, y={y}")

first, *middle, last = numbers
print(f"first={first}, middle={middle}, last={last}")

# جابجایی
a, b = 5, 10
a, b = b, a
print(f"بعد از جابجایی: a={a}, b={b}")

# تبدیل
print("\nتبدیل:")
my_list = [1, 2, 3]
my_tuple = tuple(my_list)
print(f"لیست به تاپل: {my_tuple}")

my_tuple2 = (4, 5, 6)
my_list2 = list(my_tuple2)
print(f"تاپل به لیست: {my_list2}")

# ============================================
# بخش ۲: ست (Set)
# ============================================
print("\n=== SETS ===")

# ساختن ست
fruits = {"apple", "banana", "cherry"}
numbers_set = set([1, 2, 2, 3, 3, 3, 4])

print("میوه‌ها:", fruits)
print("اعداد (بدون تکراری):", numbers_set)

# اضافه و حذف
fruits.add("orange")
fruits.update(["kiwi", "mango"])
print("\nبعد از اضافه:", fruits)

fruits.remove("banana")
fruits.discard("grape")  # خطا نمیده اگه نباشه
print("بعد از حذف:", fruits)

# عملیات ریاضی
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print("\nعملیات ریاضی:")
print(f"اجتماع (a | b): {a | b}")
print(f"اشتراک (a & b): {a & b}")
print(f"تفاضل (a - b): {a - b}")
print(f"تفاضل متقارن (a ^ b): {a ^ b}")

# بررسی
print("\nبررسی:")
print(f"1 in a: {1 in a}")
print(f"10 in a: {10 in a}")
print(f"a زیرمجموعه b: {a.issubset(b)}")
print(f"b ابرمجموعه a: {b.issuperset(a)}")

# ============================================
# بخش ۳: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱: حذف تکراری
dup = [1, 2, 2, 3, 3, 3, 4, 5, 5]
print(f"۱. بدون تکراری: {list(set(dup))}")

# تمرین ۲: اشتراک دو لیست
list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]
print(f"۲. اشتراک: {set(list1) & set(list2)}")

# تمرین ۳: مختصات
points = [(1, 2), (3, 4), (5, 6)]
import math
print("۳. فاصله نقاط از مبدأ:")
for x, y in points:
    distance = math.sqrt(x**2 + y**2)
    print(f"   ({x},{y}) → {distance:.2f}")

# تمرین ۴: اشتراک سه لیست
a = {1, 2, 3, 4}
b = {2, 3, 4, 5}
c = {3, 4, 5, 6}
print(f"۴. اشتراک سه‌تایی: {a & b & c}")

# تمرین ۵: جابجایی
x, y = 100, 200
x, y = y, x
print(f"۵. جابجایی: x={x}, y={y}")