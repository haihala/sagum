class MPlayer:
    def __init__(self, name, addr, x, y):
        self.name = name
        self.health = 100
        self.addr = addr
        self.x = x
        self.y = y

    def __repr__(self):
        return self.name + " " + self.x + " " + self.y + " " + self.health

    def __str__(self):
        return __repr__
