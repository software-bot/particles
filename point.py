class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def update(self, dx, dy):
        self.x = dx
        self.y = dy
