import time

def task_a(stop_event, name):
    print(f"{name} démarré")
    while not stop_event.is_set():
        print(f"{name} en cours d'exécution... (tâche A)")
        time.sleep(1)
    print(f"{name} arrêté proprement (tâche A)")

def task_b(stop_event, name):
    print(f"{name} démarré")
    while not stop_event.is_set():
        print(f"{name} en cours d'exécution... (tâche B)")
        time.sleep(1)
    print(f"{name} arrêté proprement (tâche B)")

def task_c(stop_event, name):
    print(f"{name} démarré")
    while not stop_event.is_set():
        print(f"{name} en cours d'exécution... (tâche C)")
        time.sleep(1)
    print(f"{name} arrêté proprement (tâche C)")
