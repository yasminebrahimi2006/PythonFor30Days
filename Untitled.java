# 📘 Python Regular Expressions (Regex) Cheat Sheet

راهنمای سریع و کاربردی برای استفاده از Regular Expressions در پایتون.

---

## 1️⃣ وارد کردن ماژول

```python
import re
```

---

## 2️⃣ توابع پرکاربرد در پایتون

| تابع | توضیح | مثال |
|------|-------|------|
| `re.match()` | فقط از **ابتدای** رشته جستجو می‌کند | `re.match(r"\d+", "123abc")` |
| `re.search()` | **هر جای** رشته را جستجو می‌کند (اولین تطابق) | `re.search(r"\d+", "abc123")` |
| `re.findall()` | **همه** تطابق‌ها را به صورت لیست برمی‌گرداند | `re.findall(r"\d+", "a1b2c3")` |
| `re.finditer()` | مثل findall ولی به صورت Iterator | `for m in re.finditer(...)` |
| `re.sub()` | جایگزینی متن | `re.sub(r"\d+", "#", "a1b2")` |
| `re.split()` | تقسیم رشته بر اساس الگو | `re.split(r"\s+", "a b  c")` |
| `re.compile()` | کامپایل الگو برای استفاده مکرر | `p = re.compile(r"\d+")` |

---

## 3️⃣ متاکاراکترها (Metacharacters)

| کاراکتر | معنی | مثال |
|---------|------|------|
| `.` | هر کاراکتری به جز newline | `a.c` → `abc`, `a1c` |
| `^` | شروع رشته | `^Hello` |
| `$` | پایان رشته | `world$` |
| `*` | صفر یا بیشتر | `ab*` → `a`, `ab`, `abb` |
| `+` | یک یا بیشتر | `ab+` → `ab`, `abb` |
| `?` | صفر یا یک (اختیاری) | `colou?r` → `color`, `colour` |
| `{n}` | دقیقاً n بار | `a{3}` → `aaa` |
| `{n,}` | n بار یا بیشتر | `a{2,}` |
| `{n,m}` | بین n تا m بار | `a{2,4}` |
| `|` | یا (OR) | `cat|dog` |
| `()` | گروه‌بندی | `(ab)+` |
| `[]` | مجموعه کاراکترها | `[abc]` |
| `\` | Escape کردن کاراکتر خاص | `\.` |

---

## 4️⃣ کلاس‌های کاراکتری (Character Classes)

| الگو | معنی |
|------|------|
| `\d` | هر رقم `[0-9]` |
| `\D` | هر چیزی غیر از رقم |
| `\w` | حرف، رقم یا آندرلاین `[a-zA-Z0-9_]` |
| `\W` | غیر از `\w` |
| `\s` | فضای خالی (space, tab, newline) |
| `\S` | غیر از فضای خالی |
| `[abc]` | یکی از a، b یا c |
| `[^abc]` | هر چیزی به جز a، b، c |
| `[a-z]` | هر حرف کوچک انگلیسی |
| `[A-Z]` | هر حرف بزرگ انگلیسی |
| `[0-9]` | هر رقم |

---

## 5️⃣ فلگ‌های مهم (Flags)

| فلگ | توضیح |
|-----|-------|
| `re.IGNORECASE` یا `re.I` | بی‌توجه به بزرگی/کوچکی حروف |
| `re.MULTILINE` یا `re.M` | `^` و `$` برای هر خط اعمال شود |
| `re.DOTALL` یا `re.S` | `.` شامل newline هم بشود |
| `re.VERBOSE` یا `re.X` | اجازه نوشتن کامنت داخل الگو |

مثال:
```python
re.findall(r"hello", text, re.IGNORECASE)
```

---

## 6️⃣ گروه‌ها (Groups)

```python
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "2024-05-20")
print(m.group())   # 2024-05-20
print(m.group(1))  # 2024
print(m.group(2))  # 05
print(m.groups())  # ('2024', '05', '20')
```

### گروه‌های نام‌دار (Named Groups)
```python
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", "2024-05")
print(m.group("year"))   # 2024
```

---

## 7️⃣ مثال‌های کاربردی

### ✅ اعتبارسنجی ایمیل
```python
pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
re.match(pattern, "test@example.com")
```

### ✅ پیدا کردن شماره تلفن
```python
re.findall(r"\d{4}-\d{4}", "تماس: 1234-5678 و 9876-5432")
```

### ✅ حذف کاراکترهای اضافی
```python
re.sub(r"[^\w\s]", "", "Hello!!! World???")
# → "Hello World"
```

### ✅ استخراج URL
```python
re.findall(r"https?://[\w\.-]+", "Visit https://google.com")
```

---

## 8️⃣ نکات مهم ⚠️

- همیشه از **Raw String** استفاده کن: `r"\d+"` نه `"\d+"`.
- برای الگوهای پیچیده از `re.compile()` استفاده کن (بهینه‌تره).
- قبل از استفاده در پروژه بزرگ، الگو رو با ابزارهایی مثل [regex101.com](https://regex101.com) تست کن.
- Regex در پایتون **Greedy** است، با `?` می‌تونی Lazy کنی: `.*?`

---

## 🔗 منابع مفید
- [مستندات رسمی پایتون](https://docs.python.org/3/library/re.html)
- [Regex101](https://regex101.com/)
- [RegexOne Tutorial](https://regexone.com/)

---

## 💬 Commit Message پیشنهادی

```bash
git add 05_strings_regex.md
git commit -m "docs: add Python regex cheat sheet"
```