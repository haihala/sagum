import socket
import ctypes
import sys

print "User is admin: ",ctypes.windll.shell32.IsUserAnAdmin()==1
try:
    UDP_IP = sys.argv[1]
except:
    UDP_IP = "127.0.0.1"
REC_PORT = 9001
SEND_PORT = 9002

r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
r.bind((UDP_IP, REC_PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP


data, addr = r.recvfrom(1024) # buffer size is 1024 bytes
print "received message:", data

if (data == "ping"):
    print "sending back pong!"
    s.sendto("pong", (UDP_IP, SEND_PORT))
