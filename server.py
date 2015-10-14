import sys
import socket
from Queue import Queue
from time import sleep
from threading import Thread

# from http://code.activestate.com/recipes/577187-python-thread-pool/
class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, clients, thread_id):
        Thread.__init__(self)
        self.clients = clients
        self.thread_id = thread_id
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            # pop an element from the queue
            (conn, data) = self.clients.get()
            # check if connection or kill request
            if conn:
                process_req(self.thread_id, conn, data, self.clients);
            else:
                break;
            # set task as done in queue
            self.clients.task_done()

# function to process a client request
def process_req(thread_id, conn, data, clients):
    sleep(0.5)
    ip, port = conn.getpeername()
    # return data to client
    conn.sendall(data)
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

# bind to port and listen for connections
s.bind(("0.0.0.0", int(sys.argv[1]))) 
s.listen(1)

# create initial workers
for i in range(min_threads): 
    Worker(clients, i)

# loop through all data received
while 1:
    # accept a connection request
    conn, addr = s.accept()
    qsize = clients.qsize()
    queue_margin = (num_threads * queue_threshold / 100)

    # check if queue size is num_threads and (num_threads - margin)
    if qsize >= (num_threads - queue_margin):
        # add queue_margin amount of new workers
        for i in range(queue_margin): 
            if num_threads == max_threads:
                break
            num_threads += 1
            Worker(clients, num_threads)
        # print to console that we're bumping the size
        if num_threads != max_threads:
            print "[MAX] bumping queue size! by " + str(queue_margin) + " to " + str(num_threads)

    # else check if queue size is between 0 and margin
    elif qsize <= queue_margin:
        # remove queue_margin amount of workers
        for i in range(queue_margin): 
            if num_threads == min_threads:
                break
            num_threads -= 1
            clients.put((None, None))
        # print to console that we're decreasing the size
        if num_threads != min_threads:
            print "[MIN] decreasing queue size! by " + str(queue_margin) + " to " + str(num_threads)

    # receive data and put request in queue
    data = conn.recv(2048)
    clients.put((conn, data))