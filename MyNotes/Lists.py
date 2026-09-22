#####   Making lists    #####-----------------------------------------------------------------
# لیست خالی
my_list = []

# لیست اعداد
numbers = [1, 2, 3, 4, 5]

# لیست رشته‌ها
fruits = ["apple", "banana", "cherry"]

# لیست ترکیبی
mixed = [1, "hello", 3.14, True]

# لیست تودرتو
matrix = [[1, 2], [3, 4], [5, 6]]



#####    Achiving items of Lists    #####----------------------------------------------------------------
fruits = ["apple", "banana", "cherry", "date"]

print(fruits[0])    # apple  (اولین)
print(fruits[1])    # banana (دومین)
print(fruits[-1])   # date   (آخرین)
print(fruits[-2])   # cherry (یکی مونده به آخر)



#####    Slicing    #####----------------------------------------------------------------
numbers = [10, 20, 30, 40, 50]

print(numbers[1:4])    # [20, 30, 40]  (از ایندکس ۱ تا ۳)
print(numbers[:3])     # [10, 20, 30]  (از اول تا ایندکس ۲)
print(numbers[2:])     # [30, 40, 50]  (از ایندکس ۲ تا آخر)
print(numbers[::2])    # [10, 30, 50]  (هر دو تا یکی)



#####    Adding     #####----------------------------------------------------------------
fruits = ["apple", "banana"]

fruits.append("cherry")        # آخر لیست
fruits.insert(1, "mango")      # توی موقعیت ۱
fruits.extend(["kiwi", "pear"]) # چند تا با هم

print(fruits)  # ['apple', 'mango', 'banana', 'cherry', 'kiwi', 'pear']


#####   Removing    #####----------------------------------------------------------------
fruits = ["apple", "banana", "cherry", "banana"]

fruits.remove("banana")   # اولین "banana" رو حذف می‌کنه
fruits.pop()              # آخرین آیتم رو حذف و برمی‌گردونه
fruits.pop(0)             # آیتم ایندکس ۰ رو حذف می‌کنه
del fruits[1]             # آیتم ایندکس ۱ رو حذف می‌کنه
fruits.clear()            # همه رو پاک می‌کنه


#####    Changing   ######-----------------------------------------------------------------
fruits = ["apple", "banana", "cherry"]
fruits[1] = "mango"
print(fruits)  # ['apple', 'mango', 'cherry']


#####   Operations  ######-----------------------------------------------------------------
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# طول لیست
print(len(numbers))         # 8

# جمع
print(sum(numbers))         # 31

# بزرگ‌ترین و کوچک‌ترین
print(max(numbers))         # 9
print(min(numbers))         # 1

# مرتب‌سازی
numbers.sort()              # صعودی
print(numbers)              # [1, 1, 2, 3, 4, 5, 6, 9]

numbers.sort(reverse=True)  # نزولی
print(numbers)              # [9, 6, 5, 4, 3, 2, 1, 1]

# معکوس کردن
numbers.reverse()
print(numbers)

# شمارش
print(numbers.count(1))     # چند تا ۱ داره

# پیدا کردن ایندکس
print(numbers.index(5))     # ایندکس عدد ۵



#####    Loops  #####----------------------------------------------------------------
fruits = ["apple", "banana", "cherry"]

# روش ۱: ساده
for fruit in fruits:
    print(fruit)

# روش ۲: با ایندکس
for i in range(len(fruits)):
    print(i, fruits[i])

# روش ۳: با enumerate (بهترین)
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")



######  Cheking Membership  #####----------------------------------------------------------------
fruits = ["apple", "banana", "cherry"]

print("apple" in fruits)      # True
print("mango" in fruits)      # False
print("mango" not in fruits)  # True



#####   Copying #####----------------------------------------------------------------
# اشتباه: این کپی نمی‌کنه، فقط یه اسم دیگه به همون لیست میده!
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4]  ← a هم تغییر کرد!

# درست: کپی واقعی
a = [1, 2, 3]
b = a.copy()
# یا
b = a[:]
b.append(4)
print(a)  # [1, 2, 3]  ← a تغییر نکرد
print(b)  # [1, 2, 3, 4]



#####   Matrix  #####----------------------------------------------------------------
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print(matrix[0][0])   # 1
print(matrix[1][2])   # 6
print(matrix[2][1])   # 8

# حلقه روی ماتریس
for row in matrix:
    for item in row:
        print(item, end=" ")
    print()



#####   List Comprehension  #####---------------------------------------------------------------
# روش معمولی
squares = []
for i in range(1, 6):
    squares.append(i ** 2)
print(squares)  # [1, 4, 9, 16, 25]

# روش لیست‌کامپرهنشن
squares = [i ** 2 for i in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# با شرط
evens = [i for i in range(1, 11) if i % 2 == 0]
print(evens)  # [2, 4, 6, 8, 10]



#####   Practicing  #####----------------------------------------------------------------
# ============ بخش ۱: ساختن لیست ============
fruits = ["apple", "banana", "cherry"]
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# ============ بخش ۲: دسترسی ============
print("اولین میوه:", fruits[0])
print("آخرین میوه:", fruits[-1])
print("سه عدد اول:", numbers[:3])

# ============ بخش ۳: اضافه کردن ============
fruits.append("orange")
fruits.insert(1, "mango")
print("بعد از اضافه کردن:", fruits)

# ============ بخش ۴: حذف کردن ============
fruits.remove("banana")
fruits.pop()
print("بعد از حذف:", fruits)

# ============ بخش ۵: عملیات ============
print("طول لیست:", len(numbers))
print("جمع:", sum(numbers))
print("بزرگ‌ترین:", max(numbers))
print("کوچک‌ترین:", min(numbers))

# ============ بخش ۶: مرتب‌سازی ============
numbers.sort()
print("مرتب صعودی:", numbers)

numbers.sort(reverse=True)
print("مرتب نزولی:", numbers)

# ============ بخش ۷: حلقه ============
print("\nحلقه روی میوه‌ها:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

# ============ تمرین‌ها ============
print("\n=== تمرین‌ها ===")

# تمرین ۱: جمع
my_numbers = [10, 20, 30, 40, 50]
print(f"جمع: {sum(my_numbers)}")

# تمرین ۲: مرتب‌سازی
friends = ["Ali", "Sara", "Reza", "Maryam"]
friends.sort()
print(f"دوستای مرتب: {friends}")

# تمرین ۳: بزرگ‌ترین و کوچک‌ترین
nums = [5, 12, 3, 45, 7, 19, 2]
print(f"بزرگ‌ترین: {max(nums)}, کوچک‌ترین: {min(nums)}")

# تمرین ۴: حذف تکراری
dup = [1, 2, 2, 3, 4, 4, 5, 5, 5]
print(f"بدون تکراری: {list(set(dup))}")

# تمرین ۵: میانگین
grades = [18, 17, 19, 20, 15]
print(f"میانگین: {sum(grades)/len(grades):.2f}")

