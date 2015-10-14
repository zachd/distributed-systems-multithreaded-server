import socket
import sys
from time import sleep
from random import randrange

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set GET message
data = "helo\n"

# connect to server and send messag
for i in range(1000):
    print "sending" + str(i)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 61234)) 
    s.sendall(data)

# print sent and received data
received = s.recv(1024)
print "Sent:     {}".format(data)
print "Received: {}".format(received)