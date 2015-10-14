import socket
import sys
from time import sleep
from random import randrange

# set GET message
data = "HELO asd\n"

for i in range(1000):
    print "Sending #" + str(i)
    # connect to socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 61234)) 
    # send data
    s.sendall(data)
    # print received response
    received = s.recv(1024)
    print "Received: {}".format(received)
