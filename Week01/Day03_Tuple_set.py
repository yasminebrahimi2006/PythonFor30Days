# تاپل
coordinates = (10, 20)
colors = ("red", "green", "blue")

# دسترسی
print(coordinates[0])

# unpacking
x, y = coordinates
print(x, y)

# تاپل تک‌عضوی 
single = (5,)   # کاما لازمه

# ست###############################
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}

# اضافه/حذف
fruits.add("orange")
fruits.remove("banana")

# عملیات ریاضی
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)   # اجتماع (union)
print(a & b)   # اشتراک (intersection)
print(a - b)   # تفاضل (difference)

# حذف تکراری از لیست
my_list = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(my_list))
print(unique)   # [1, 2, 3, 4]