class Cart:
    def __init__(self):
        self.goods = []  # Список товаров

    def add(self, gd):
        self.goods.append(gd)

    def remove(self, indx):
        if 0 <= indx < len(self.goods):
            del self.goods[indx]

    def get_list(self):
        return [f"{item.name}: {item.price}" for item in self.goods]

class Table:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class TV:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Notebook:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cup:
    def __init__(self, name, price):
        self.name = name
        self.price = price

cart = Cart()

cart.add(TV("Samsung QLED", 150000))
cart.add(TV("LG OLED", 120000))
cart.add(Table("Деревянный стол", 8000))
cart.add(Notebook("MacBook AIR", 200000))
cart.add(Notebook("ASUS TUF", 150000))
cart.add(Cup("Пластиковая кружка", 500))

for item in cart.get_list():
    print(item)