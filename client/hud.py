import pygame

class Popup:
    def __init__(self, msg, size):
        length = int((size[0]*2/3)/18)
        msgl = []
        msgl += list(msg[0+i:length+i] for i in range(0, len(msg), length))
        self.font = pygame.font.SysFont("monospace", 25)
        self.font.set_bold(True)
        self.surface = pygame.Surface((size[0]*2/3, size[1]*2/3))
        self.pos = (size[0]/6, size[1]/6)
        self.surface.fill((205, 133, 63))
        pygame.draw.rect(self.surface, (0, 0, 0), pygame.rect.Rect(0, 0, size[0]*3/2, size[1]*3/2), 2)
        for i in range(len(msgl)):
            text = self.font.render(msgl[i], 1, (0, 0, 0))
            self.surface.blit(text, (self.surface.get_size()[0]/2-self.font.size(msgl[i])[0]/2, 10 + i*30))

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
    def __init__(self, player, size, color, surface):
        self.surface = surface
        self.ms = pygame.font.SysFont("monospace", 25)
        self.ms.set_bold(True)
        self.player = player
        self.color = color
        self.interfaces = {}
        self.size = size

        self.interfaces["health"] = Interface(str(self.player.health), self.color, self.ms, "health", self.size)
        self.interfaces["target"] = Interface("No targets yet", self.color, self.ms, "target", self.size)
        self.interfaces["ammo"] = Interface("0 / 0", self.color, self.ms, "ammo", self.size)

    def display(self):
        for i in self.interfaces:
            for o in range(len(self.interfaces[i].pos)):
                if o == len(self.interfaces[i].pos) - 1:
                    self.surface.blit(self.interfaces[i].img, self.interfaces[i].pos[o])
                else:
                    self.surface.blit(self.interfaces[i].outline, self.interfaces[i].pos[o])

    def update(self, cdict):
        for ikey in self.interfaces:
            for dkey in cdict:
                if ikey == dkey:
                    self.interfaces[ikey] = Interface(cdict[dkey], self.color, self.ms, dkey, self.size)

        # peru brown 205,133,63
