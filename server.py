import socket
import ctypes
import sys
import time
import threading
import player


entities = [] # a list containing all the entities currently in the game.
players = []  # -"- players in the game
socket.setdefaulttimeout(0.05)

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
    tell("Started to knit and started a new thread with console handeling.")

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
    for i in range(100000): # test loop to find out what can a normal pc do in 1/20 s.
        a = 100000**100000

def tell(message):
    """A nicer print, determines the module printing the message."""
    subject = "Server"
    if __name__ != "__main__":
        subject = __name__
    print "[" + subject + "]", message
    sendAll("[" + subject + "]" + message)

def sendAll(msg):
    """Send message to all clients."""
    global players
    global s
    for p in players:
        s.sendto("msg", p.ip)

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

        inp = raw_input(">")
        inp = inp.lower()
        inp = inp.split()
        i = inp[0][0]
        if i == "h":
            tell("Help is on its way, just hold on!")
        elif i == "q":
            tell("Are you sure you want to quit? (y/n)")
            if (raw_input(">")[0].lower() == "y"):
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

"""
import socket
import ctypes
import sys
import time


socket.setdefaulttimeout(0.05)
if(ctypes.windll.shell32.IsUserAnAdmin()==1):
    print "User is very supery"
else:
    print "User is a puny mortal"

try:
    UDP_IP = sys.argv[1]
except:
    UDP_IP = "127.0.0.1"
FROM_CLIENT_PORT = 9001
TO_CLIENT_PORT = 9002

r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
r.bind((UDP_IP, FROM_CLIENT_PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
print "Ready to play!"

while 1:
    try:
        data, addr = r.recvfrom(1024) # buffer size is 1024 bytes
    except socket.timeout:
        data = ""
    if data != "":
        print "received message:", data, " from:", addr

    if (data == "ping"):
        print "sending back pong!"
        s.sendto("pong", (addr[0], TO_CLIENT_PORT))
"""
