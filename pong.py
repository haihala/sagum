import socket
import sys

try:
    UDP_IP = sys.argv[1]
except IndexError:
    UDP_IP = "127.0.0.1"

SEND_PORT = 9001
REC_PORT = 9002
MESSAGE = "ping"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
s.sendto(MESSAGE, (UDP_IP, SEND_PORT))

r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
r.bind((UDP_IP, REC_PORT))

data, addr = r.recvfrom(1024) # buffer size is 1024 bytes
print "received message:", data

if (data == "pong"):
    print "sending back ping!"
    s.sendto("ping", (UDP_IP, SEND_PORT))
