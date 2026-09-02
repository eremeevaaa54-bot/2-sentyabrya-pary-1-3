class Car:
    def __init__(self):
        self._engine_temperature = 20

    def start_engine(self):
        self._engine_temperature = 90
        print("двигатель прогрет")

    def drive(self):
        if self._engine_temperature >= 90:
            print("поехали!")
        else:
            print("двигатель не прогрет")


my_car = Car()

print("температура:", my_car._engine_temperature)
my_car.drive()
my_car.start_engine()
my_car.drive()
print("температура:", my_car._engine_temperature)