'''
import socket

s = socket.socket()
print("Socket successfully created")

port = 12345

s.bind(('', port))
print(f"Server binded to {port}")

s.listen(5)
print("Server is listening")

ip_addrs = {'192.16.5.12': [0, 0], '128.65.2.81': [0, 0], '10.0.15.1': [0, 0]}

while True:
    c, addr = s.accept()
    print(f"Got connection from {addr}")
    # message = c.recv(1024)
    # print("Recieved message: ", message.decode('utf8'))
    new_ip = None
    for key, val in ip_addrs.items():
        if val[0] == 0:
            new_ip = key
            ip_addrs[key][0] = 1                    # set IP as 'being used'
            ip_addrs[key][1] = addr                 # save conn's data with IP
            print(f"Assigning IP: {new_ip} to {addr}")
            msg = new_ip
            break
    else:
        print("No IP available to assign...")
        msg = "IP address not available. Try after some time..."
    c.send(msg.encode('utf8'))

    try:
        data = c.recv(1024).decode('utf8')
    except:
        print(f"Connection closed by {addr}")
        for k, v in ip_addrs.items():
            if v[1] == addr:
                v[0] = 0                # release IP
                break
        c.close()

'''
import socket
import sys
import threading
import time
import random
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
SERVER_SIZE = 3
queue = Queue()
all_connections = []
all_address = []

ip_addrs = {'.'.join(map(str,[random.randint(10, 150) for _ in range(4)])): [0, 0] for x in range(SERVER_SIZE)}


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(SERVER_SIZE)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    print("List of random IPs generated: ")
    print(ip_addrs)
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        for ind, c in enumerate(all_connections):
            try:
                c.send("Connection alive".encode('utf8'))
            except Exception as e:
                # print(f"Exception occured: {e}")
                all_connections.pop(ind)
                add = all_address.pop(ind)
                for k, v in ip_addrs.items():
                    if v[1] == add:
                        v[0] = 0
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            new_ip = None
            for key, val in ip_addrs.items():
                if val[0] == 0:
                    new_ip = key
                    ip_addrs[key][0] = 1                    # mark IP as 'being used'
                    ip_addrs[key][1] = address              # save conn's data with IP
                    print(f"\nConnection established with: {address}, Assigning IP: {new_ip}")
                    msg = new_ip
                    conn.send(msg.encode('utf8'))
                    break
            else:
                print(f"\nConnection req. from {address}, but No IP available to assign...Dropping")
                conn.close()

        except Exception as e:
            print(f"Error accepting connections, {e}")


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
