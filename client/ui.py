import pygame

class Interface:
    def __init__(self, content, color, font, pos, ss):
        self.img = font.render(content, 1, color)
        self.outline = font.render(content, 1, (0, 0, 0))
        if pos == "health":
            pos = (ss[0]/2 - font.size(content)[0]/2, 5)
        elif pos == "target":
            pos = (5, 5)
        elif pos == "ammo":
            pos = (ss[0] - font.size(content)[0] - 5, ss[1] - font.size(content)[1] - 5)
        self.pos = ((pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]+1), pos)

class Ui:
    def __init__(self, player, size, color):
        self.ms = pygame.font.SysFont("monospace", 25)
        self.ms.set_bold(True)
        self.player = player
        self.color = color
        self.interfaces = {}
        self.size = size

        self.interfaces["health"] = Interface(str(self.player.health), self.color, self.ms, "health", self.size)
        self.interfaces["target"] = Interface("No target system yet", self.color, self.ms, "target", self.size)
        self.interfaces["ammo"] = Interface("0 / 0", self.color, self.ms, "ammo", self.size)

    def display(self, surface):
        for i in self.interfaces:
            for o in range(len(self.interfaces[i].pos)):
                if o == len(self.interfaces[i].pos) - 1:
                    surface.blit(self.interfaces[i].img, self.interfaces[i].pos[o])
                else:
                    surface.blit(self.interfaces[i].outline, self.interfaces[i].pos[o])

    def update(self, cdict):
        for ikey in self.interfaces:
            for dkey in cdict:
                if ikey == dkey:
                    self.interfaces[ikey] = Interface(cdict[dkey], self.color, self.ms, dkey, self.size)
