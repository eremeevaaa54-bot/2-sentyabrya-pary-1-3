TYPE_OS = 1  # 1 - Windows; 2 - Linux

class DialogWindows:
    name_class = "DialogWindows"

class DialogLinux:
    name_class = "DialogLinux"

class Dialog:
    def __new__(cls, name):
        if TYPE_OS == 1:
            obj = super().__new__(DialogWindows)
        else:
            obj = super().__new__(DialogLinux)
        obj.name = name
        return obj

dlg = Dialog("Моё окно")
print(type(dlg).__name__) 
print(dlg.name)            
print(dlg.name_class)      

TYPE_OS = 2
dlg2 = Dialog("Окно Linux")
print(type(dlg2).__name__)  
print(dlg2.name)            
print(dlg2.name_class)     
