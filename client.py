

"""
import socket
import sys
from game import *

socket.setdefaulttimeout(0.05)

try:
    UDP_IP = sys.argv[1]
except IndexError:
    UDP_IP = "127.0.0.1"

TO_SERVER_PORT = 9001
FROM_SERVER_PORT = 9002
MESSAGE = "ping"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
s.sendto(MESSAGE, (UDP_IP, TO_SERVER_PORT))

r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
r.bind((UDP_IP, FROM_SERVER_PORT))

game = Game()
game.setup()
game.daemon = True
game.start()

time.sleep(0.01)
while 1:
    time.sleep(0.1)
    if game.end == True:
        print "stop"
        game.join()
        sys.exit()

while 1:
    try:
        data, addr = r.recvfrom(1024) # buffer size is 1024 bytes
    except socket.timeout:
        data = ""
    if data != "":
        print "received message:", data, " from:", addr

    if (data == "pong"):
        print "sending back ping"
        s.sendto("ping", (addr[0], TO_SERVER_PORT))
"""
