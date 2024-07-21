import random
import threading
import time
from anim_mt import StoppableThread, r, c, t
import queue


def cmdlistener(cmd_queue):
    commands = ["r 5", "c 5", "t 5", "r 5", "c 5"]  # Example commands
    for command in commands:
        time.sleep(random.randint(3, 6))  # Simulate receiving commands at random intervals
        cmd_queue.put(command)
        #print(f"Command received: {command}")


def handle_cmd(task_queue, command, duration, stop_event):
    if command == "r":
        task_queue.put((r, duration))
    elif command == "c":
        task_queue.put((c, duration))
    elif command == "t":
        stop_event.set()
        # vider les commandes précédentes
        while not task_queue.empty():
            task_queue.get()
        # configurer commande thunder
        task_queue.put((t, duration))
        task_queue.put(("stop",))


def cmdhandler(cmd_queue, task_queue, stop_event):
    while True:
        cmd = cmd_queue.get()
        # print(cmd)
        command, duration = cmd.split()
        handle_cmd(task_queue, command, duration, stop_event)


def taskexecutor(task_queue, stop_event):
    CT = None
    while True:
        task_data = task_queue.get()
        if task_data[0] == "stop":
            if CT and CT.is_alive():
                stop_event.set()
                CT.join()
                stop_event.clear()
        else:
            if CT and CT.is_alive():
                CT.join()
            CT = StoppableThread(task=task_data[0], stop_event=stop_event, duration=int(task_data[1]))
            CT.start()


def main():
    stop_event = threading.Event()
    cmd_queue = queue.Queue()
    task_queue = queue.Queue()

    listener_thread = threading.Thread(target=cmdlistener, args=(cmd_queue,))
    handler_thread = threading.Thread(target=cmdhandler, args=(cmd_queue, task_queue, stop_event,))
    executor_thread = threading.Thread(target=taskexecutor, args=(task_queue, stop_event,))

    listener_thread.start()
    handler_thread.start()
    executor_thread.start()

    listener_thread.join()
    handler_thread.join()
    executor_thread.join()


if __name__ == "__main__":
    main()
