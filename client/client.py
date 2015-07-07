import pygame
import math
from player import *
import socket
import threading
import object
from mapper import *

x = pygame.init()
if not x == (6, 0):
    print "Failed pygame init"
    sys.exit(1)

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
            settings["windowsize"] = i
        elif j == "I":
            settings["ip"] = i[0]
        elif j == "U":
            settings["username"] = i[0]
        elif j == "M":
            settings["map"] = i[0]

print settings
players = []
objects = loadMap(settings["map"])
for o in objects: o.img = pygame.image.load("art/structures/"+o.img)
serverMap = "Sg_def.map"
ns = 30  # Normal Speed
mapsize = 10000
screensize = 400
ut = 0  # updatetimer used in printing update as a delay.
swm = settings["windowsize"][0]/screensize  # screen width multiplier
shm = settings["windowsize"][1]/screensize  # screen height multiplier

gameDisplay = pygame.display.set_mode(settings["windowsize"])
pygame.display.set_caption("Sagum")

gameExit = False  # When true, window closes
p = Player(settings["username"], 10, 10, 100)  # Normal player object
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
                if event.key == pygame.K_LEFT:
                    p.speed[0] -= ns
                if event.key == pygame.K_RIGHT:
                    p.speed[0] += ns
                if event.key == pygame.K_UP:
                    p.speed[1] -= ns
                if event.key == pygame.K_DOWN:
                    p.speed[1] += ns
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    p.speed[0] += ns
                if event.key == pygame.K_RIGHT:
                    p.speed[0] -= ns
                if event.key == pygame.K_UP:
                    p.speed[1] += ns
                if event.key == pygame.K_DOWN:
                    p.speed[1] -= ns

        if settings["map"] != serverMap:
            p.pos = [10, 10]
            objects = loadMap(settings["map"])
            for o in objects: o.img = pygame.image.load("art/structures/"+o.img)

        if math.sqrt(p.speed[0]**2+p.speed[1]**2) > ns:
            move = math.sqrt(1.0/2)*ns
        else:
            move = ns

        if p.pos[0] + p.speed[0] > 0 and p.pos[0] + p.speed[0] < mapsize and not p.speed[0] == 0:
            p.pos[0] += math.copysign(1, p.speed[0]) * move
        if p.pos[1] + p.speed[1] > 0 and p.pos[1] + p.speed[1] < mapsize and not p.speed[1] == 0:
            p.pos[1] += math.copysign(1, p.speed[1]) * move

        if p.pos[0] >= screensize/2 and p.pos[0] <= mapsize - screensize/2:
            p.drawpos[0] = settings["windowsize"][0]/2
        else:
            if p.pos[0] >= mapsize - screensize/2:
                p.drawpos[0] = (p.pos[0] - (mapsize-screensize)) * swm
            else:
                p.drawpos[0] = p.pos[0] * swm

        if p.pos[1] >= screensize/2 and p.pos[1] <= mapsize - screensize/2:
            p.drawpos[1] = settings["windowsize"][1]/2
        else:
            if p.pos[1] >= mapsize - screensize/2:
                p.drawpos[1] = (p.pos[1] - (mapsize-screensize)) * shm
            else:
                p.drawpos[1] = p.pos[1] * shm

        screenRect = pygame.Rect(0, 0, screensize, screensize)

        gradiant = math.sqrt(p.pos[0]**2 + p.pos[1]**2) / math.sqrt(2*mapsize**2)
        gameDisplay.fill((39 * gradiant, 180 - (111 * gradiant), 19 * gradiant))  # at bottom right corner 39,69,19 at start 0, 200, 0
        hsc = screensize / 2  # screen sized

        for i in players:
            print "drawing players"
            pygame.draw.rect(gameDisplay, (0, 0, 0), [i.drawpos[0], i.drawpos[1], i.size, i.size])

        for i in objects:
            print "drawing object"
            gameDisplay.blit(i.img, (i.pos[0] + hsc - max(p.pos[0], hsc), i.pos[1] + hsc - max(p.pos[1], hsc)))

        pygame.draw.rect(gameDisplay, (0, 0, 0), [p.drawpos[0], p.drawpos[1], p.size, p.size])
        pygame.display.update()
        s.sendto("update " + str(p.pos[0]) + " " + str(p.pos[1]) , (settings["ip"], 9001))
        """
        ut += 1
        if ut == 60:
            print p.pos, p.drawpos, p.speed
            ut = 0
        """
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
