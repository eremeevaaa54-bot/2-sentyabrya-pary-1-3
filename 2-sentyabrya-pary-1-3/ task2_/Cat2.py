class Cat:
    def __init__(self, breed, name, age):
        self.breed = breed
        self.name = name
        self.age = age

    def draw(self):
        print(f"на экране рисуется кот {self.name}, порода {self.breed}")


cat1 = Cat("шотландская", "Шуля", 5)
cat2 = Cat("Сиамская", "Кася", 12)
cat3 = Cat("дворнняга", "Тимоша", 10)

print(f"{cat1.name}, {cat1.breed}, {cat1.age}")
print(f"{cat2.name}, {cat2.breed}, {cat2.age}")
print(f"{cat3.name}, {cat3.breed}, {cat3.age}")

cat1.draw()
cat2.draw()
cat3.draw()