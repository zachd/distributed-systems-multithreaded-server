Distributed Systems - Lab 2
=====
> Student ID: f01f3533cd97ebd24e7c1b49639a2c3c2fd904c9e6a105226ecde32db16d0b10

Creates a server that uses smart thread pooling to respond to client requests.

## Start server
    >sh start.sh {port_num}

## Send message
    >python client.py {port_num} HELO {message} \\n

## Kill server
    >python client.py {port_num} KILL_SERVICE\\n