class CPU:
    def __init__(self, name, fr):
        self.name = name
        self.fr = fr


class Memory:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume


class MotherBoard:
    def __init__(self, name, cpu, *mem_slots):
        self.name = name
        self.cpu = cpu
        self.total_mem_slots = 4
        self.mem_slots = list(mem_slots[:self.total_mem_slots])

    def get_config(self):
        mem_str = '; '.join([f"{mem.name} - {mem.volume}" for mem in self.mem_slots])

        return [
            f'Материнская плата: {self.name}',
            f'Центральный процессор: {self.cpu.name}, {self.cpu.fr}',
            f'Слотов памяти: {self.total_mem_slots}',
            f'Память: {mem_str}'
        ]

cpu = CPU("AMD RYZEN 9 9950x3D", "3.4 GHz")
mem1 = Memory("Kingston", "2000 GB")
mem2 = Memory("Samsung", "32 GB")
mb = MotherBoard("ASUS TUF GAMING B850", cpu, mem1, mem2)

config = mb.get_config()

for line in config:
    print(line)