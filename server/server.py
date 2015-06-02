import socket
import ctypes
import sys
import time
import threading
import mplayer
import pygame


entities = [] # a list containing all the entities currently in the game.
players = []  # -"- players in the game
socket.setdefaulttimeout(0.05)
s = ""
r = ""

def start():
    """Called at startup. Initializes everything"""
    tell("Good morning, I will be your server.")
    global entities
    tell("Firing up ye ol' genny to produce some entities.")
    entities = generateEntities()
    tell("Entities generated, trying to open sockets. Sockets have nothing to do with socks, which is confusing.")
    global s, r
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Sending socket

    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Receiving socket (same socket can not listen and send)
    r.bind(("127.0.0.1", 9001)) # Server is listening port 9001 and sending on 9002. Ip is localhost for obvious reasons.
    tell("Found my old lasso and bound port 9001 to listening mode.")

    global consoleThread
    consoleThread.daemon = True
    consoleThread.start()

    tell("Started to knit and started new threads for console handeling and interwebbing.")

    tell("Preparing to run like Usain Bolt.")
    runLoop()

def runLoop():
    """The main loop of the server. It is managing ticks and messaging. In case of a 'quit' command it shuts down the server."""
    global entities
    global players
    lastsec = lasttick = time.time()
    tickCount = 0
    skipticks = 0
    tell("Running.")
    global kill
    while 1:
        if (kill):
            sys.exit(2)

        if lastsec + 1 <= time.time():
            lastsec = time.time()
            if (tickCount < 20):
                tell("skipped " + str(20 - tickCount) + " ticks this second.")
            tickCount = 0

        if lasttick + 0.047 < time.time() and tickCount <= 20:
            lasttick = time.time()
            tickCount += 1
            tick()

def tick():
    """One update that is supposed to make the game go forwards. Happens about 20 times per second"""
    global r
    global s
    global players
    clock = pygame.time.Clock()
    while 1:
        try:
            data, addr = r.recvfrom(1024)
            data = data.split()
            if data[0] == "login":
                tell(data[1] + " has just joined our lovely little session")
                print data[1], addr, data[2], data[3]
                players.append(mplayer.MPlayer(data[1], addr[0], data[2], data[3]))
                tell("currently playing: ")
                tell(players)
                sendAll("server " + data[1] + " has just joined our lovely little session")
            elif data[0] == "move":
                for p in players:
                    if p.addr == addr[0]:
                        p.x = data[1]
                        p.y = data[2]
            elif data[0] == "leave":
                for i in players:
                    if p.addr = addr[0]:
                        players.remove(p)

        except socket.timeout:
            pass

        for p in players:
            sendAll(p)
        clock.tick(20)

def tell(message):
    """A nicer print, determines the module printing the message."""
    global players
    if message == players:
        for i in players:
            print i.name
        return
    subject = "Server"
    if __name__ != "__main__":
        subject = __name__
    print "[" + subject + "]", message

def sendAll(msg):
    """Send message to all clients."""
    global players
    global s
    for p in players:
        s.sendto("msg", (p.addr, 9002))

def generateEntities():
    """Fill server entities list with items, players, mobs, etc."""
    return []


def consolehandler():
    """This function is ran on a thread. It keeps the console running."""
    time.sleep(1)
    global kill
    while 1:
        if (kill):
            break

        inp = raw_input()
        inp = inp.lower()
        inp = inp.split()
        i = inp[0][0]
        if i == "h":
            tell("Help is on its way, just hold on!")
        elif i == "q":
            tell("Are you sure you want to quit? (y/n)")
            if (raw_input()[0].lower() == "y"):
                tell("Shutting down...")
                kill = True


if __name__ == "__main__":
    if(ctypes.windll.shell32.IsUserAnAdmin()==0):
        tell("Please restart your terminal/cmd/shell/bash as administrator")
        tell("Puny mortal")
        sys.exit(0)
    else:
        tell("User is very supery and quite administrative")

    consoleThread = threading.Thread(target=consolehandler)

    kill = False
    start()
