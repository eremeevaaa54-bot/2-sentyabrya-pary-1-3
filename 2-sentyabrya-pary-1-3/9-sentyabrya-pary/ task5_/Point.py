class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color

p1 = Point(10, 20)
p2 = Point(12, 5, 'green')
p3 = Point(-3, 7, 'pink')
points = [p1, p2, p3]

for p in points:
    print(p.x, p.y, p.color)