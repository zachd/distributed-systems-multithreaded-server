import socket
import sys
from time import sleep
from random import randrange

if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    sys.exit("Port number required")

# set GET message
if len(sys.argv) > 2:
    data = ' '.join(map(str, sys.argv[2:]))
else:
    data = "HELO test message\n"

for i in range(1000):
    print "Sending #" + str(i) + ": \"" + data + "\""
    # connect to socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", int(sys.argv[1]))) 
    # send data
    s.sendall(data)
    # print received response
    received = s.recv(1024)
    print "Received: {}".format(received)
