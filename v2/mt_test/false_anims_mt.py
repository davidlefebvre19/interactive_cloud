import time

def task_a(stop_event, name, duration):
    print(f"{name} démarré")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print(f"{name} en cours d'exécution...")
        time.sleep(1)
    if stop_event.is_set:
        print("Thread stopped by stop event")
    print(f"{name} arrêté proprement")

def task_b(stop_event, name, duration):
    print(f"{name} démarré")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print(f"{name} en cours d'exécution...")
        time.sleep(1)
    if not stop_event.is_set:
        print("Thread stopped by duration NOT stop event")
    print(f"{name} arrêté proprement")

def task_c(stop_event, name, duration):
    print(f"{name} démarré")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print(f"{name} en cours d'exécution...")
        time.sleep(1)
    if not stop_event.is_set:
        print("Thread stopped by duration NOT stop event")
    print(f"{name} arrêté proprement")