import threading
import time



class StoppableThread(threading.Thread):
    def __init__(self, task, stop_event, duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = task
        self.stop_event = stop_event
        self.duration = duration

    def run(self):
        self.task(self.stop_event, self.duration)

def r(stop_event, duration):
    print(f"Animation rainbow démarrée pour {duration} secondes")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode rainbow...")
        time.sleep(1)
    print("Animation rainbow terminée")

def c(stop_event, duration):
    print(f"Animation chill démarrée pour {duration} secondes")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode chill...")
        time.sleep(1)
    print("Animation chill terminée")

def t(stop_event, duration):
    print(f"Animation thunder démarrée pour {duration} secondes")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode thunder...")
        time.sleep(1)
    print("Animation thunder terminée")