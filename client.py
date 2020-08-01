'''
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
s.connect(('127.0.0.1', port))

# message = 'Hello!'.encode('utf8')
# s.send(message)
ip = s.recv(1024).decode('utf8')
print(f"IP assigned to this client: {ip}")
while True:
    inp = input("Enter q to terminate: ")
    if inp == 'q':
        # close the connection
        s.send("quit".encode('utf8'))
        s.close()
        break
'''
import socket
import os
import subprocess

s = socket.socket()
host = '127.0.0.1'
port = 9999

s.connect((host, port))

ip = s.recv(1024).decode('utf8')
print(f"Got assigned IP: {ip}")

while True:
    try:
        data = s.recv(1024).decode('utf8')
        if not data:
            print("Connection unavailable")
            break
        print(data)
    except Exception as e:
        print(f"Connection unavailble")
        s.close()
        break
