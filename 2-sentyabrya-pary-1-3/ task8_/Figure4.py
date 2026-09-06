class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

    def draw(self):
        print("рисуется фигура")

class Line(Figure):
    def __init__(self, coords, width, color, length):
        super().__init__(coords, width, color)
        self.length = length

    def draw(self):
        print("рисуется линия")

class Rect(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height

    def draw(self):
        print("рисуется прямоугольник")

class Ellipse(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius

    def draw(self):
        print("рисуется эллипс")

class Triangle(Figure):
    def __init__(self, coords, width, color, side1, side2, side3):
        super().__init__(coords, width, color)
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def draw(self):
        print("рисуется треугольник")

line = Line((0, 0), 1, "оранжевый", 10)
rect = Rect((3, 4), 2, "лаймовый", 7)
ellipse = Ellipse((-2, -3), 1, "тифани", 6)
triangle = Triangle((5, 5), 3, "синий", 4, 5, 6)  # НОВЫЙ ОБЪЕКТ

figures = [line, rect, ellipse, triangle]

for figure in figures:
    figure.draw()