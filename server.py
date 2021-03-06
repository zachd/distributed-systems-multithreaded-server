import sys
import socket
import re
from Queue import Queue
import thread
from threading import Thread

# Worker class from http://code.activestate.com/recipes/577187-python-thread-pool/
class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, clients):
        Thread.__init__(self)
        # store clients queue pointer
        self.clients = clients
        # set as daemon so it dies when main thread exits
        self.daemon = True
        # start the thread on init
        self.start()
    
    def run(self):
        while True:
            # pop an element from the queue
            (conn, data) = self.clients.get()
            # check if connection or kill request
            if conn:
                process_req(conn, data)
            else:
                break;
            # set task as done in queue
            self.clients.task_done()

# function to process a client request
def process_req(conn, data):
    ip, port = conn.getsockname()
    print "\"" + data + "\""
    match = re.match("HELO (.*)\\n", data)
    # check if kill command or helo message
    if data == "KILL_SERVICE\\n":
        thread.interrupt_main()
    elif match is not None:
        conn.sendall("HELO " + match.groups()[0] + "\nIP:" + ip + "\nPort:" + str(port) + "\nStudentID:f01f3533cd97ebd24e7c1b49639a2c3c2fd904c9e6a105226ecde32db16d0b10\n")
    # close connection
    conn.close()

if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    sys.exit("Port number required")

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# max and min number of threads
max_threads = 100
min_threads = 5

# thread counter
num_threads = min_threads

# queue threshold to increase or decrease num workers
queue_threshold = 30

# queue object to store requests
clients = Queue()

# current ip (http://stackoverflow.com/a/9481595)
from urllib2 import urlopen
my_ip = urlopen('http://ip.42.pl/raw').read()

# bind to port and listen for connections
s.bind((my_ip, int(sys.argv[1]))) 
print "[start] binding to " + my_ip + ":" + sys.argv[1]
s.listen(1)

# create initial workers
for _ in range(min_threads): 
    Worker(clients)

# continuous loop to keep accepting requests
while 1:
    # accept a connection request
    conn, addr = s.accept()

    # cache queue size and get threshold
    qsize = clients.qsize()
    queue_margin = (num_threads * queue_threshold / 100)

    # check if queue size is num_threads and (num_threads - margin)
    if qsize >= (num_threads - queue_margin):
        # add queue_margin amount of new workers
        for _ in range(queue_margin): 
            if num_threads == max_threads:
                break
            Worker(clients)
            num_threads += 1
        # print to console that we're bumping the size
        if num_threads != max_threads:
            print "[MAX] bumping queue size! by " + str(queue_margin) + " to " + str(num_threads)
    # else check if queue size is between 0 and margin
    elif qsize <= queue_margin:
        # remove queue_margin amount of workers
        for _ in range(queue_margin): 
            if num_threads == min_threads:
                break
            clients.put((None, None))
            num_threads -= 1
        # print to console that we're decreasing the size
        if num_threads != min_threads:
            print "[MIN] decreasing queue size! by " + str(queue_margin) + " to " + str(num_threads)

    # receive data and put request in queue
    data = conn.recv(2048)
    clients.put((conn, data))
