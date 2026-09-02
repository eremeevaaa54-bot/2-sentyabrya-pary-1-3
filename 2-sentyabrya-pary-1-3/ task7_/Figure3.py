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

line = Line((0, 0), 1, "ораньжевый", 10)
rect = Rect((3, 4), 2, "лаймовый", 7)
ellipse = Ellipse((-2, -3), 1, "тифани", 6)

figures = [line, rect, ellipse]

for figure in figures:
    figure.draw()