import pygame

class Popup:
    def __init__(self, msg, size):
        self.font = pygame.font.SysFont("monospace", 25)
        self.font.set_bold(True)
        self.surface = pygame.Surface((size[0]/2, size[1]/2))
        self.pos = (size[0]/4, size[1]/4)
        self.surface.fill((205, 133, 63))
        pygame.draw.rect(self.surface, (0, 0, 0), pygame.rect.Rect(0, 0, size[0]/2, size[1]/2), 2)
        textSize = self.font.size(msg)
        if textSize[0] < size[0]/2 and textSize[1] < size[1]/2:
            text = self.font.render(msg, 1, (0, 0, 0))
            self.surface.blit(text, (size[0]/4-textSize[0]/2, size[1]/4-textSize[1]/2))



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
