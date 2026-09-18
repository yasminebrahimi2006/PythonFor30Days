# ساختن لیست
fruits = ["apple", "banana", "cherry"]

# اضافه کردن
fruits.append("orange")           # آخر لیست
fruits.insert(1, "mango")         # توی موقعیت خاص

# حذف کردن
fruits.remove("banana")           # با مقدار
fruits.pop()                      # آخرین آیتم
fruits.pop(0)                     # با ایندکس

# دسترسی
print(fruits[0])                  # اولین
print(fruits[-1])                 # آخرین
print(fruits[1:3])                # برش (slice)

# مرتب‌سازی
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()                    # صعودی
numbers.sort(reverse=True)        # نزولی

# طول
print(len(numbers))

# حلقه روی لیست
for fruit in fruits:
    print(fruit)