class Player():
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.speed = [0, 0]
        self.size = 10
        self.health = 100

    def __repr__(self):
        return self.name + " " + str(self.x) + " " + str(self.y) + " " + str(self.health)

    def __str__(self):
        return self.name + " " + str(self.x) + " " + str(self.y) + " " + str(self.health)
