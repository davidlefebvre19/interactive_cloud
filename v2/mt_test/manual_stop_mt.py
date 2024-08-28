import random
import threading
import time
from false_anims_mt import task_a, task_b, task_c

# Création des threads
class StoppableThread(threading.Thread):
    def __init__(self, name, lock, stop_event, task, duration,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.lock = lock
        self.stop_event = stop_event
        self.task = task  # Stockage de la référence de la fonction, pas son exécution
        self.duration = duration

    def run(self):
        with self.lock:
            self.task(self.stop_event, self.name, self.duration)  # Appel de la tâche spécifiée

# Fonction pour démarrer et arrêter les threads séquentiellement
def run_threads_sequentially():
    lock = threading.Lock()
    stop_event = threading.Event()

    """""
    # Création des instances de threads avec des tâches spécifiques
    threads = [
        StoppableThread("Thread A", lock, stop_event, task_a),
        StoppableThread("Thread B", lock, stop_event, task_b),
        StoppableThread("Thread C", lock, stop_event, task_c)
    ]


    for thread in threads:
        # stop_event.clear()  # Réinitialiser l'événement d'arrêt
        thread.start()
        time.sleep(5)  # Laisser le thread fonctionner pendant 5 secondes
        stop_event.set()  # Signal pour arrêter le thread
        thread.join()  # Attendre que le thread se termine proprement
    """""

    tasks =[task_a, task_b, task_c]

    for i in range(4):
        duration = random.randint(5, 8)
        print("duration: " + str(duration))
        t = StoppableThread("Thread "+str(i), lock, stop_event, random.choice(tasks), duration)
        if i == 1:
            stop_event.set()
        t.start()
        t.join()