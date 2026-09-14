class DataBase:
    lst_data = []
    FIELDS = ('id', 'name', 'old', 'salary')

    def insert(self, data):
        for row in data:
            values = row.split()
            record = {}
            for i in range(len(self.FIELDS)):
                record[self.FIELDS[i]] = values[i]
            self.lst_data.append(record)

    def select(self, a, b):
        if b >= len(self.lst_data):
            b = len(self.lst_data) - 1
        return self.lst_data[a:b + 1]

lst_in = [
    "1 Сергей 35 120000",
    "2 Федор 23 12000",
    "3 Иван 13 1200"
]
db = DataBase()
db.insert(lst_in)

for record in db.lst_data:
    print(record)

print("\nВыборка [0:1]:")
for record in db.select(0, 1):
    print(record)