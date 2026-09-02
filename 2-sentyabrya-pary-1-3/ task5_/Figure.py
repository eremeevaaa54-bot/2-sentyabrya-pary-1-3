class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color

fig = Figure((10, 20), 5, "винный")
print(fig.coords, fig.width, fig.color)