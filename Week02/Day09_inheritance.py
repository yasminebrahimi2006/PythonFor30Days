from abc import ABC, abstractmethod
import math

# ============================================
# بخش ۱: وراثت پایه
# ============================================
print("=== وراثت پایه ===")

class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "..."
    
    def info(self):
        return f"من {self.name} هستم"

class Dog(Animal):
    def speak(self):
        return f"{self.name} میگه: واق واق!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} میگه: میو میو!"

dog = Dog("Rex")
cat = Cat("Whiskers")
print(dog.info())
print(dog.speak())
print(cat.speak())

# ============================================
# بخش ۲: super()
# ============================================
print("\n=== super() ===")

class Animal2:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def info(self):
        return f"{self.name} ({self.age} ساله)"

class Dog2(Animal2):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    
    def info(self):
        return f"{super().info()} - نژاد: {self.breed}"

dog2 = Dog2("Rex", 3, "German Shepherd")
print(dog2.info())

# ============================================
# بخش ۳: وراثت چندسطحی
# ============================================
print("\n=== وراثت چندسطحی ===")

class Creature:
    def eat(self):
        return "داره غذا می‌خوره"

class Mammal(Creature):
    def feed_milk(self):
        return "داره شیر میده"

class Dog3(Mammal):
    def bark(self):
        return "واق واق"

dog3 = Dog3()
print(dog3.eat())
print(dog3.feed_milk())
print(dog3.bark())

# ============================================
# بخش ۴: وراثت چندگانه
# ============================================
print("\n=== وراثت چندگانه ===")

class Swimmer:
    def swim(self):
        return "شنا می‌کنه"

class Flyer:
    def fly(self):
        return "پرواز می‌کنه"

class Duck(Swimmer, Flyer):
    def quack(self):
        return "کواک کواک"

duck = Duck()
print(duck.swim())
print(duck.fly())
print(duck.quack())

# ============================================
# بخش ۵: پلی‌مورفیسم
# ============================================
print("\n=== پلی‌مورفیسم ===")

class Shape:
    def area(self):
        return 0
    
    def describe(self):
        return f"مساحت: {self.area():.2f}"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2

shapes = [Circle(5), Square(4)]
for shape in shapes:
    print(f"{shape.__class__.__name__}: {shape.describe()}")

# ============================================
# بخش ۶: کلاس انتزاعی
# ============================================
print("\n=== کلاس انتزاعی ===")

class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand
    
    @abstractmethod
    def move(self):
        pass

class Car(Vehicle):
    def move(self):
        return f"{self.brand} داره رانندگی می‌کنه"

class Plane(Vehicle):
    def move(self):
        return f"{self.brand} داره پرواز می‌کنه"

car = Car("Toyota")
plane = Plane("Boeing")
print(car.move())
print(plane.move())

# ============================================
# بخش ۷: مثال کاربردی - دستگاه‌های شبکه
# ============================================
print("\n=== دستگاه‌های شبکه ===")

class Device:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
    
    def ping(self):
        return f"پینگ {self.ip}"
    
    def info(self):
        return f"{self.name} ({self.ip})"

class Router(Device):
    def ping(self):
        return f"پینگ روتر {self.ip}: موفق"
    
    def route(self, destination):
        return f"مسیریابی به {destination}"

class Switch(Device):
    def ping(self):
        return f"پینگ سوییچ {self.ip}: موفق"
    
    def list_ports(self, count):
        return f"{count} پورت فعال"

class Firewall(Device):
    def ping(self):
        return f"پینگ فایروال {self.ip}: بلاک شده!"

devices = [
    Router("router1", "192.168.1.1"),
    Switch("switch1", "192.168.1.2"),
    Firewall("fw1", "192.168.1.3")
]

for device in devices:
    print(f"{device.info()}: {device.ping()}")

# ============================================
# بخش ۸: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱: حیوانات
animals = [Dog("Rex"), Cat("Whiskers")]
print("۱. حیوانات:")
for a in animals:
    print(f"   {a.speak()}")

# تمرین ۲: وسایل نقلیه
class Vehicle2:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed
    
    def info(self):
        return f"{self.brand} - {self.speed} km/h"

class Car2(Vehicle2):
    def __init__(self, brand, speed, doors):
        super().__init__(brand, speed)
        self.doors = doors
    
    def info(self):
        return f"{super().info()} - {self.doors} در"

class Bike(Vehicle2):
    def __init__(self, brand, speed, type_):
        super().__init__(brand, speed)
        self.type = type_
    
    def info(self):
        return f"{super().info()} - {self.type}"

vehicles = [Car2("Toyota", 180, 4), Bike("Giant", 30, "کوهستان")]
print("۲. وسایل نقلیه:")
for v in vehicles:
    print(f"   {v.info()}")

# تمرین ۳: کارمندان
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def calculate_salary(self):
        return self.salary

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus
    
    def calculate_salary(self):
        return self.salary + self.bonus

class Intern(Employee):
    def calculate_salary(self):
        return self.salary * 0.5

employees = [
    Employee("Ali", 5000),
    Manager("Sara", 8000, 2000),
    Intern("Reza", 3000)
]
print("۳. کارمندان:")
for emp in employees:
    print(f"   {emp.name}: {emp.calculate_salary()}")

# تمرین ۴: دستگاه‌های شبکه
print("۴. دستگاه‌های شبکه:")
for device in devices:
    print(f"   {device.connect() if hasattr(device, 'connect') else device.ping()}")

# تمرین ۵: شکل‌ها
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
print("۵. شکل‌ها:")
for shape in shapes:
    print(f"   {shape.__class__.__name__}: {shape.describe()}")