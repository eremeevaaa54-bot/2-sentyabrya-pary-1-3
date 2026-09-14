class AbstractClass:
    def __new__(cls):
        return "Ошибка: нельзя создавать объекты абстрактного класса"

# Проверка
obj = AbstractClass()
print(obj)
