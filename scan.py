import socket
import threading
from queue import Queue
import sys
import time
from datetime import datetime

lock = threading.Lock()

target = input("IP:") # Input for ip address 

queue = Queue()

openports = [] #saving the open ports here


def portscan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        out = s.connect_ex((target, port))
        if out == 0:
            with lock:
                    print("\nopen port:", port)
                    openports.append(port)
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

with open(f"scan_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", 'w') as f: #saving the data into a file with the name of the file being the date
    f.write(f"Scan results for {target} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("Open ports:\n")
    for port in openports:
        f.write(f"{port}\n")