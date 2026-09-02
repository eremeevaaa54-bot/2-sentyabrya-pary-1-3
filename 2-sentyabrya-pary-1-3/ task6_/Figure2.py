class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

class Line(Figure):
    def __init__(self, coords, width, color, length):
        super().__init__(coords, width, color)
        self.length = length

class Rect(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height

class Ellipse(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius

line = Line((5, 7), 3, "коричневый", 15)
rect = Rect((-4, 2), 4, "чернный", 12)
ellipse = Ellipse((8, -6), 2, "пурпурный", 9)

print(f"Line: {line.coords}, {line.width}, {line.color}, {line.length}")
print(f"Rect: {rect.coords}, {rect.width}, {rect.color}, {rect.height}")
print(f"Ellipse: {ellipse.coords}, {ellipse.width}, {ellipse.color}, {ellipse.radius}")