class Player():
    def __init__(self, name, x, y, health):
        self.name = name
        self.pos = [x, y]
        self.drawpos = self.pos[:]
        self.speed = [0, 0]
        self.size = 10
        self.health = health

    def __repr__(self):
        return self.name + " " + str(self.pos[0]) + " " + str(self.pos[1]) + " " + str(self.health)

    def __str__(self):
        return self.name + " " + str(self.pos[0]) + " " + str(self.pos[1]) + " " + str(self.health)
