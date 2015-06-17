import pygame
import math
from player import *
import socket

x = pygame.init()
if not x == (6, 0):
    print "Failed pygame init"
    sys.exit(1)

settings = {}
o = open("cs.txt", "r")
o = o.read().split("\n")
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

print settings
ns = 0.5  # Normal Speed
mapsize = 10000
screensize = 100
ut = 0  # updatetimer used in printing update as a delay.
swm = settings["windowsize"][0]/screensize  # screen width multiplier
shm = settings["windowsize"][1]/screensize  # screen height multiplier

print swm, shm
gameDisplay = pygame.display.set_mode(settings["windowsize"])
pygame.display.set_caption("The game")

gameExit = False  # When true, window closes
p = Player(settings["username"], 10, 10)  # Normal player object
clock = pygame.time.Clock()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Sending socket

r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Receiving socket socket
r.bind(("127.0.0.1", 9002)) # Server is listening port 9001 and sending on 9002. Ip is localhost for obvious reasons.

loginpacket = "login " + str(p)
print loginpacket
s.sendto(loginpacket, (settings["ip"], 9001))

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

        gameDisplay.fill((255, 255, 255))
        pygame.draw.rect(gameDisplay, (0, 0, 0), [p.drawpos[0], p.drawpos[1], p.size, p.size])
        pygame.display.update()
        s.sendto("update " + str(p.pos[0]) + " " + str(p.pos[1]) , (settings["ip"], 9001))
        ut += 1
        if ut == 60:
            print p.pos, p.drawpos, p.speed
            ut = 0
    except KeyboardInterrupt:
        gameExit = True

    clock.tick(60)

s.sendto("leave", (settings["ip"], 9001))
pygame.quit()
quit()
