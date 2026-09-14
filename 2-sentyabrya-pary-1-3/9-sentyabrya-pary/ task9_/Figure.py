class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

    def draw(self):
        print("Рисуется фигура")

class Line(Figure):
    def __init__(self, coords, width, color, length):
        super().__init__(coords, width, color)
        self.length = length

    def draw(self):
        print("Рисуется линия")

class Rect(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height

    def draw(self):
        print("Рисуется прямоугольник")

class Ellipse(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius

    def draw(self):
        print("Рисуется эллипс")

class Triangle(Figure):
    def __init__(self, coords, width, color, side1, side2, side3):
        super().__init__(coords, width, color)
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def draw(self):
        print("Рисуется треугольник")

line = Line((0, 0), 1, "красный", 10)
rect = Rect((3, 4), 2, "зеленый", 7)
ellipse = Ellipse((-2, -3), 1, "желтый", 6)

figures = [line, rect, ellipse]

print("До добавления треугольника")
for figure in figures:
    figure.draw()

triangle = Triangle((5, 5), 3, "синий", 4, 5, 6)
figures.append(triangle)  # Просто добавляем!

print("\nПосле добавления треугольника")
for figure in figures:
    figure.draw()