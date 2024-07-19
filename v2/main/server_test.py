import socket
import threading

host = '127.0.0.1'
port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if not data:
            break

        print(data.decode())