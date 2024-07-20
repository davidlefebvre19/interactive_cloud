import threading
import time
from false_anims_mt import task_a, task_b, task_c

# Création des threads
class StoppableThread(threading.Thread):
    def __init__(self, name, lock, stop_event, task, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.lock = lock
        self.stop_event = stop_event
        self.task = task  # Stockage de la référence de la fonction, pas son exécution

    def run(self):
        with self.lock:
            self.task(self.stop_event, self.name)  # Appel de la tâche spécifiée

# Fonction pour démarrer et arrêter les threads séquentiellement
def run_threads_sequentially():
    lock = threading.Lock()
    stop_event = threading.Event()

    # Création des threads avec des tâches spécifiques et des durées
    task_a_thread = StoppableThread("Thread A", lock, stop_event, task_a, 5)  # 5 secondes pour tâche A
    task_b_thread = StoppableThread("Thread B", lock, stop_event, task_b, 5)  # 5 secondes pour tâche B
    task_c_thread = StoppableThread("Thread C", lock, stop_event, task_c, 5)  # 5 secondes pour tâche C

    # Démarrage de task_a
    task_a_thread.start()
    task_a_thread.join()  # Attendre la fin de task_a

    # Démarrage de task_b
    task_b_thread.start()
    time.sleep(3)  # Laisser task_b fonctionner pendant 3 secondes
    stop_event.set()  # Activer stop_event pour interrompre task_b
    task_b_thread.join()  # Attendre que task_b se termine

    # Démarrage de task_c
    task_c_thread.start()
    task_c_thread.join()  # Attendre que task_c se termine

run_threads_sequentially()

print("Tous les threads ont été exécutés et arrêtés.")