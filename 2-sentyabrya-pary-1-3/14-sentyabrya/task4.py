class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def clone(self):
        return Point(self.x, self.y)

pt = Point(3, 7)
pt_clone = pt.clone()

print(f"pt: x={pt.x}, y={pt.y}")
print(f"pt_clone: x={pt_clone.x}, y={pt_clone.y}")
print(f"Это разные объекты: {pt is not pt_clone}")
