import threading
from anim_mt import StoppableThread, r, c, t
import queue
import socket

host = '127.0.0.1'
port = 65432


def cmdlistener(cmd_queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("client connected to server : listening")
        while True:
            data = s.recv(1024)

            if not data:
                break

            if len(data.decode().split()) == 2:
                #print(data.decode())
                #print(type(data.decode()))
                cmd_queue.put(data.decode())


def handle_cmd(task_queue, command, duration):
    if command == "r":
        task_queue.put((r, duration))
    elif command == "c":
        task_queue.put((c, duration))
    elif command == "t":
        #stop_event.set()
        # vider les commandes précédentes
        print("Commande thunder recue, suppression des commandes restantes !!!")
        i = 0
        while not task_queue.empty():
            task_queue.get()
            i += 1
        #stop_event.clear()
        print(str(i) + " commandes supprimées")
        # configurer commande thunder
        task_queue.put(("stop",))
        task_queue.put((t, duration))


def cmdhandler(cmd_queue, task_queue):
    print("cmd handler start")
    while True:
        cmd = cmd_queue.get()
        # print(cmd)
        command, duration = cmd.split()
        handle_cmd(task_queue, command, duration)


def taskexecutor(task_queue, stop_event):
    print("executor start")
    CT = None
    while True:
        task_data = task_queue.get()
        if task_data[0] == "stop":
            if CT and CT.is_alive():
                print("interuption de l'animation actuelle !")
                stop_event.set()
                print("stop event set")
                CT.join()
                stop_event.clear()
                print("stop event cleared")
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
    handler_thread = threading.Thread(target=cmdhandler, args=(cmd_queue, task_queue,))
    executor_thread = threading.Thread(target=taskexecutor, args=(task_queue, stop_event,))

    listener_thread.start()
    handler_thread.start()
    executor_thread.start()

    listener_thread.join()
    handler_thread.join()
    executor_thread.join()


if __name__ == "__main__":
    main()
