import socket
import threading
import random
import time

# Paramètres du serveur socket
host = '127.0.0.1'
port = 65432


class AnimationController(threading.Thread):

    def __init__(self, stop_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chill = True
        self.animationRunning = False
        self.animationThread = None
        self.stop_event = stop_event

    def thunder(self):
        pass

    def calm(self):
        pass

    def rain(self):
        pass

    def stop(self):
        pass

    def run_animations(self):
        pass


animationController = AnimationController()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if not data:
            break

        print(data.decode())
