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
