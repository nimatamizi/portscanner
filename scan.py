import socket
import threading
from queue import Queue
import sys
import time


lock = threading.Lock()

target = input("IP:")

queue = Queue()

def portscan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        out = s.connect_ex((target.port))
        if out == 0:
            with lock:
                    print("port open :", port)
        s.close()
    except:
        pass

def worker():
    while True:
        port= queue.get()
        portscan(port)
        queue.task_done()
threads = 100

for thread in range(threads):
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()

start = int(input("Start port:"))
end = int(input("End port:"))

for port in range(start, end + 1):
    queue.put(port)

try:
    for _ in range(start, end + 1):
        sys.stdout.flush()
        time.sleep(0.05) #thats for the loading bar adjustment
        sys.stdout.write('\rScanning ports: [{0:50s}] {1:.1f}%'.format('#' * int((_ - start + 1) * 50 / (end - start + 1)), (_ - start + 1) * 100 / (end - start + 1))) #loading bar
finally:
    queue.join()

print('scanning is done.')