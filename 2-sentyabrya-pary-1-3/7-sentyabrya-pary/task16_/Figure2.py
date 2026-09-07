import random

class Line:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Rect:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Ellipse:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

elements = []

for _ in range(217):
    a = random.randint(-100, 100)
    b = random.randint(-100, 100)
    c = random.randint(-100, 100)
    d = random.randint(-100, 100)

    class_type = random.choice([Line, Rect, Ellipse])

    elements.append(class_type(a, b, c, d))

for obj in elements:
    if isinstance(obj, Line):
        obj.sp = (0, 0)
        obj.ep = (0, 0)

print(f"Всего объектов: {len(elements)}")
print(f"Объектов Line: {sum(1 for obj in elements if isinstance(obj, Line))}")
print(f"Объектов Rect: {sum(1 for obj in elements if isinstance(obj, Rect))}")
print(f"Объектов Ellipse: {sum(1 for obj in elements if isinstance(obj, Ellipse))}")

print("\nПервые 5 объектов:")
for i, obj in enumerate(elements[:5]):
    print(f"{i + 1}. {type(obj).__name__}: sp={obj.sp}, ep={obj.ep}")