# ============================================
# بخش ۱: اولین کلاس
# ============================================
print("=== اولین کلاس ===")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"سلام، من {self.name} هستم و {self.age} سالمه."

person1 = Person("Yasmin", 20)
person2 = Person("Ali", 25)

print(person1.greet())
print(person2.greet())

# ============================================
# بخش ۲: ویژگی کلاس
# ============================================
print("\n=== ویژگی کلاس ===")

class User:
    count = 0
    
    def __init__(self, name):
        self.name = name
        User.count += 1

u1 = User("Yasmin")
u2 = User("Ali")
u3 = User("Reza")
print(f"تعداد کاربران: {User.count}")

# ============================================
# بخش ۳: متدهای مختلف
# ============================================
print("\n=== متدها ===")

class MathUtils:
    @staticmethod
    def is_even(n):
        return n % 2 == 0
    
    @staticmethod
    def is_positive(n):
        return n > 0

print(f"4 زوجه؟ {MathUtils.is_even(4)}")
print(f"-5 مثبته؟ {MathUtils.is_positive(-5)}")

# ============================================
# بخش ۴: متدهای جادویی
# ============================================
print("\n=== متدهای جادویی ===")

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self):
        return f"'{self.title}' نوشته‌ی {self.author}"
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    def __len__(self):
        return self.pages

book = Book("1984", "George Orwell", 328)
print(str(book))
print(repr(book))
print(f"تعداد صفحات: {len(book)}")

# ============================================
# بخش ۵: کلاس Server (کاربردی)
# ============================================
print("\n=== کلاس Server ===")

class Server:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.is_running = False
    
    def start(self):
        self.is_running = True
        return f"{self.name} شروع شد روی {self.ip}:{self.port}"
    
    def stop(self):
        self.is_running = False
        return f"{self.name} متوقف شد"
    
    def status(self):
        state = "روشن" if self.is_running else "خاموش"
        return f"{self.name}: {state}"
    
    def __str__(self):
        return f"Server({self.name}, {self.ip}:{self.port})"

server1 = Server("web-server", "192.168.1.1", 80)
server2 = Server("db-server", "192.168.1.2", 5432)

print(server1.start())
print(server1.status())
print(server2.status())
print(server1)

# ============================================
# بخش ۶: کلاس APIClient (کاربردی)
# ============================================
print("\n=== کلاس APIClient ===")

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        return f"GET {url}"
    
    def post(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        return f"POST {url} با data: {data}"

client = APIClient("https://api.example.com", "my-secret-key")
print(client.get("users"))
print(client.post("users", {"name": "Yasmin"}))

# ============================================
# بخش ۷: تمرین‌ها
# ============================================
print("\n=== تمرین‌ها ===")

# تمرین ۱: Student
class Student:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades
    
    def average(self):
        return sum(self.grades) / len(self.grades)
    
    def __str__(self):
        return f"{self.name} ({self.age}) - معدل: {self.average():.2f}"

s = Student("Yasmin", 20, [18, 17, 19])
print(f"۱. {s}")

# تمرین ۲: Calculator
class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

calc = Calculator()
calc.add(5, 3)
calc.add(10, 20)
print(f"۲. تاریخچه: {calc.history}")

# تمرین ۳: BankAccount
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount):
        self.balance += amount
        return f"واریز {amount}. موجودی: {self.balance}"
    
    def withdraw(self, amount):
        if amount > self.balance:
            return "موجودی کافی نیست!"
        self.balance -= amount
        return f"برداشت {amount}. موجودی: {self.balance}"
    
    def __str__(self):
        return f"حساب {self.owner}: {self.balance}"

acc = BankAccount("Yasmin", 1000)
print(f"۳. {acc.deposit(500)}")
print(f"   {acc.withdraw(200)}")
print(f"   {acc}")

# تمرین ۴: User برای API
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_active = True
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active
        }
    
    def __str__(self):
        status = "فعال" if self.is_active else "غیرفعال"
        return f"{self.username} ({self.email}) - {status}"

user = User("yasmin", "yasmin@example.com")
print(f"۴. {user}")
print(f"   {user.to_dict()}")

# تمرین ۵: Server Ping
class NetworkServer:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.running = False
    
    def start(self):
        self.running = True
    
    def ping(self):
        if self.running:
            return f"پینگ {self.ip}: موفق"
        return f"پینگ {self.ip}: سرور خاموشه"

ns = NetworkServer("web1", "192.168.1.1")
ns.start()
print(f"۵. {ns.ping()}")