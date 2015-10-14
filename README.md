Distributed Systems - Lab 2
=====

Creates a server that uses smart thread pooling to respond to client requests.

## Start server
    >sh start.sh {port_num}

## Send message
    >python client.py {port_num} HELO {message} \\n

## Kill server
    >python client.py KILL_SERVICE\\n