# لیستی از دیکشنری‌ها
students = [
    {"name": "Ali", "age": 20, "grades": [18, 17, 19]},
    {"name": "Sara", "age": 22, "grades": [20, 19, 18]},
    {"name": "Reza", "age": 21, "grades": [15, 16, 14]},
]

# میانگین هر دانش‌آموز
for student in students:
    avg = sum(student["grades"]) / len(student["grades"])
    print(f"{student['name']}: {avg:.2f}")

# دیکشنری با مقادیر لیست
classes = {
    "math": ["Ali", "Sara"],
    "physics": ["Reza", "Sara"],
    "chemistry": ["Ali", "Reza"]
}

for subject, students_list in classes.items():
    print(f"{subject}: {len(students_list)} students")