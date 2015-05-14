import socket
import ctypes
import sys
import time

entities = [] # a list containing all the entities of the game.
players = []
socket.setdefaulttimeout(0.05)

def start():
    """Called at startup. Initializes everything"""
    tell("Good morning, I will be your server.")
    global entities
    tell("Firing up ye ol' genny to produce some entities.")
    entities = generateEntities()
    tell("Entities generated, trying to open sockets. Sockets have nothing to do with socks, which is confusing.")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Sending socket

    r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Receiving socket (same socket can not listen and send)
    r.bind(("127.0.0.1", 9001)) # Server is listening port 9001 and sending on 9002. Ip is localhost for obvious reasons.
    tell("Found my old lasso and bound port 9001 to listening mode.")

    tell("Preparing to run like Usain Bolt.")
    runLoop()

def runLoop():
    global entities
    global players
    lastsec = time.time()
    tickCount = 0
    tell("Running.")
    while 1:
        if lastsec + 1 <= time.time():
            lastsec = time.time()
            if (tickCount < 20):
                tell("skipped " + str(20 - tickCount) + " ticks this second")
            tickCount = 0

        if (tickCount >= 20):
            time.sleep(0.01)
        else:
            tickCount += 1
            tick()

def tick():
    pass

def tell(message):
    """A nicer print, determines the module printing the message."""
    subject = "Server"
    if __name__ != "__main__":
        subject = __name__
    print "[" + subject + "]", message
    sendAll("[" + subject + "]" + message)

def sendAll(msg):
    """Send message to all clients."""
    pass

def generateEntities():
    """Fill server entities list with items, players, mobs, etc."""
    return []

def consolehandler():
    while 1:
        inp = raw_input(">")
        inp = inp.lowercase
        inp = inp[0]
        if inp == "h":
            tell("Help is on the way, just hold on!")


if __name__ == "__main__":
    if(ctypes.windll.shell32.IsUserAnAdmin()==0):
        tell("Please restart your terminal/cmd/shell/bash as administrator")
        tell("Puny mortal")
        sys.exit(0)
    else:
        tell("User is very supery and quite administrative")
    tell(str(time.time()))
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
