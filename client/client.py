from pygame.rect import *
import pygame
import math
from player import *
import socket
import threading
import object
from mapper import *
from ui import *

x = pygame.init()
if not x == (6, 0):
    print "Failed pygame init"
    sys.exit(1)

def collides(a):  # returns a boolean, if a collides with any object
    global objects
    for o in objects:
        if a.colliderect(o.rect):
            return True
    return False


def receiver():
    rclock = pygame.time.Clock()
    global players
    while 1:
        data, addr = r.recvfrom(1024)
        if data.split()[0] == "map":
            try:
                settings["map"] = data.split()[1:].join()
                objects = loadMap(settings["map"])
            except maploadError:
                print "Failed to load map for reasons unknown."
        else:
            data = data[1:-1].split(",")
            for p in players:
                for i in data:
                    if p.name == i[0]:
                        p.pos = [i[1], i[2]]
                        p.health = i[3]
                        data.remove(i)
                if len(data) == 0:
                    break
            if len(data) != 0:
                for i in data:
                    if i.split()[0] == settings["username"]:
                        data.remove(i)
                    elif i[0] == "[":
                        print i
                    else:
                        players.append(Player(i[0], i[1], i[2], i[3]))
        rclock.tick(60)

settings = {}
a = open("cs.txt", "r")
o = a.read().split("\n")
a.close()
for i in o:
    if len(i) > 0 and not i[0] == "#":
        i = i.split()
        j = i.pop(0)
        if j == "S":
            i = map(int, i)
            i = tuple(i)
            settings["windowSize"] = i
        elif j == "I":
            settings["ip"] = i[0]
        elif j == "C":
            settings["uiColor"] = tuple(map(int, i))
        elif j == "U":
            settings["username"] = i[0]
        elif j == "M":
            settings["map"] = i[0]

print settings
players = []
objects = loadMap(settings["map"])
for o in objects:
    o.img = pygame.image.load("art/structures/"+o.img)
    o.rect = Rect(o.pos, o.img.get_size())
    wd = 800 / settings["windowSize"][0]
    hd = 800 / settings["windowSize"][1]
    pygame.transform.scale(o.img, (o.img.get_width()*wd, o.img.get_height()*hd))

serverMap = "Sg_def.smap"
ns = 3  # Normal Speed
mapsize = 10000
mapRect = Rect(0, 0, mapsize, mapsize)

screensize = 400
ut = 0  # updatetimer used in printing update as a delay.

gameDisplay = pygame.display.set_mode(settings["windowSize"])
pygame.display.set_caption("Sagum")

gameExit = False  # When true, window closes
p = Player(settings["username"], 10, 10, 100)  # Normal player object
ui = Ui(p, settings["windowSize"], settings["uiColor"])  # definition of ui, uses player stats
clock = pygame.time.Clock()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Sending socket

r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Receiving socket socket
r.bind(("127.0.0.1", 9002)) # Server is listening port 9001 and sending on 9002. Ip is localhost for obvious reasons.

loginpacket = "login " + str(p)
s.sendto(loginpacket, (settings["ip"], 9001))

rt = threading.Thread(target=receiver)  # receiverthread is responsible for picking up the packets servers throws at us.
rt.daemon = True
rt.start()

while not gameExit:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    p.speed[0] -= 1
                if event.key == pygame.K_d:
                    p.speed[0] += 1
                if event.key == pygame.K_w:
                    p.speed[1] -= 1
                if event.key == pygame.K_s:
                    p.speed[1] += 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    p.speed[0] += 1
                if event.key == pygame.K_d:
                    p.speed[0] -= 1
                if event.key == pygame.K_w:
                    p.speed[1] += 1
                if event.key == pygame.K_s:
                    p.speed[1] -= 1

        if settings["map"] != serverMap:
            p.pos = [10, 10]
            objects = loadMap(settings["map"])
            for o in objects:
                o.img = pygame.image.load("art/structures/"+o.img)
                o.rect = Rect(o.pos, o.img.get_size())
                wd = 800 / settings["windowSize"][0]
                hd = 800 / settings["windowSize"][1]
                pygame.transform.scale(o.img, (o.img.get_width()*wd, o.img.get_height()*hd))

        if math.sqrt(p.speed[0]**2+p.speed[1]**2) > 1 and not p.pushed:
            move = math.sqrt(1.0/2)*ns
        else:
            move = ns

        newRect = False
        if p.speed[0] != 0 and p.speed[1] != 0:
            newRect = Rect((p.pos[0] + math.copysign(1, p.speed[0]) * move, p.pos[1] + math.copysign(1, p.speed[1]) * move), p.rect.size)

        elif p.speed[0] != 0:
            newRect = Rect((p.pos[0] + math.copysign(1, p.speed[0]) * move, p.pos[1]), p.rect.size)

        elif p.speed[1] != 0:
            newRect = Rect((p.pos[0], p.pos[1] + math.copysign(1, p.speed[1]) * move), p.rect.size)

        if newRect:
            if mapRect.colliderect(newRect) and not collides(newRect):
                p.pos[0] = newRect.x
                p.pos[1] = newRect.y


        p.drawpos = (settings["windowSize"][0]/2, settings["windowSize"][1]/2)

        gradiant = math.sqrt(p.pos[0]**2 + p.pos[1]**2) / math.sqrt(2*mapsize**2)
        hsc = screensize / 2  # half of screen size
        gameDisplay.fill((0, 0, 0))
        paintRect = Rect((settings["windowSize"][0]/2 - p.pos[0], settings["windowSize"][1]/2 - p.pos[1]), mapRect.size)
        gameDisplay.fill((39 * gradiant, 180 - (111 * gradiant), 19 * gradiant), rect=paintRect)  # at bottom right corner 39,69,19 at start 0, 200, 0
        p.rect = pygame.rect.Rect(p.pos, (10, 10))

        for i in players:
            pygame.draw.rect(gameDisplay, (0, 0, 0), [i.drawpos[0], i.drawpos[1], i.size, i.size])

        for i in objects:
            gameDisplay.blit(i.img, (i.pos[0] - p.pos[0] + settings["windowSize"][0]/2, i.pos[1] - p.pos[1] + settings["windowSize"][1]/2))

        pygame.draw.rect(gameDisplay, (0, 0, 0), [p.drawpos[0], p.drawpos[1], p.size, p.size])

        ui.update({"health": str(p.health)})
        ui.display(gameDisplay)
        pygame.display.update()

        s.sendto("update " + str(p.pos[0]) + " " + str(p.pos[1]) , (settings["ip"], 9001))

        ut += 1
        if ut == 60:
            print p.pos, p.speed, clock.get_fps()
            ut = 0

    except KeyboardInterrupt:
        gameExit = True
    """
    except Exception as e:
        print e
        gameExit = True
    """
    clock.tick(60)

s.sendto("leave", (settings["ip"], 9001))
pygame.quit()
quit()
