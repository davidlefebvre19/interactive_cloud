import threading
import time

class StoppableThread(threading.Thread):
    def __init__(self, name, lock, stop_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.lock = lock
        self.stop_event = stop_event

    def run(self):
        with self.lock:
            print(f"{self.name} démarré")
            while not self.stop_event.is_set():
                print(f"{self.name} en cours d'exécution...")
                time.sleep(1)
            print(f"{self.name} arrêté proprement")

# Fonction pour démarrer et arrêter les threads séquentiellement
def run_threads_sequentially():
    lock = threading.Lock()
    stop_event = threading.Event()

    threads = [
        StoppableThread("Thread A", lock, stop_event),
        StoppableThread("Thread B", lock, stop_event),
        StoppableThread("Thread C", lock, stop_event)
    ]

    for thread in threads:
        stop_event.clear()  # Reset stop event
        thread.start()
        time.sleep(5)  # Laisser le thread fonctionner pendant 5 secondes
        stop_event.set()  # Signal pour arrêter le thread
        thread.join()  # Attendre que le thread se termine proprement

run_threads_sequentially()

print("Tous les threads ont été exécutés séquentiellement.")