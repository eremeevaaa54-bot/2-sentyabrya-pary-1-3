class Figure:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_coords(self):
        return self._x, self._y

    def set_coords(self, x, y):
        self._x = x
        self._y = y


class Circle(Figure):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def calculate_area(self):
        return 3.14 * self.radius * self.radius


class Square(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y)
        self.side = side

    def calculate_area(self):
        return self.side * self.side

figures = [
    Circle(0, 0, 5),
    Square(3, 4, 4),
    Circle(-2, 3, 3),
    Square(-5, -2, 6),
    Circle(10, 10, 2)
]

total_area = 0

for figure in figures:
    area = figure.calculate_area()
    total_area += area
    print(f"Площадь: {area}")

print(f"\nОбщая площадь всех фигур: {total_area}")