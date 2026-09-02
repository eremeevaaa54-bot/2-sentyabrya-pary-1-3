class Graph:
    def __init__(self, x, y, scale):
        self._x = x
        self._y = y
        self._scale = scale

    def move(self, dx, dy):
        self._x += dx
        self._y += dy
        print(f"график перемещен на ({dx}, {dy})")

    def change_scale(self, factor):
        self._scale *= factor
        print(f"масштаб изменен в {factor} раз")

    def show(self):
        print(f"график: x={self._x}, y={self._y}, масштаб={self._scale}")

graph1 = Graph(0, 0, 1)
graph2 = Graph(5, 10, 2)
graph3 = Graph(-3, 7, 1.5)

print("начальное состтояние")
graph1.show()
graph2.show()
graph3.show()

print("\nперемещаем 1 график")
graph1.move(3, -2)

print("\nизменям моштаб 2")
graph2.change_scale(2.5)

print("\nитоговое состояни")
graph1.show()
graph2.show()
graph3.show()