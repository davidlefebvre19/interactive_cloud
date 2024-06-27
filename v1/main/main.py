import socket
import threading
import random
import numpy as np
import usb.core
import time
from art import *

# Paramètres du serveur socket
host = '127.0.0.1'
port = 65432
# Paramètres micro
AMA0 = usb.core.find(idVendor=0x16c0, idProduct=0x5dc)
wait = 0.5
min_db = 10
storm_trigger = 10
# FIFO arrays for db values
avg_db = np.zeros(30)
inst_db = np.zeros(6)
# animations
anims = ["raindrop ", "calm "]
auto_anims = ["raindrop ", "calm ", "thunder "]


def read_db():
    ret = AMA0.ctrl_transfer(0xC0, 4, 0, 0, 200)
    return float((ret[0] + ((ret[1] & 3) * 256)) * 0.1 + 30)


def fill_values(wait):
    global avg_db
    global inst_db
    # fill avg and inst
    for i in range(len(avg_db)):
        avg_db = np.roll(avg_db, -1)
        dB = read_db()
        avg_db[-1] = dB
        time.sleep(wait)
    for i in range(len(inst_db)):
        inst_db = np.roll(inst_db, -1)
        dB = read_db()
        inst_db[-1] = dB
        time.sleep(wait)
    return avg_db, inst_db


def update_db():
    global avg_db
    global inst_db
    #print(avg_db)
    avg_db = np.roll(avg_db, -1)
    avg_db[-1] = read_db()
    #print(avg_db)
    #print(inst_db)
    inst_db = np.roll(inst_db, -1)
    inst_db[-1] = read_db()
    #print(inst_db)
    print("Current noise:")
    print(str(int(np.mean(inst_db))) + " dB")
    return np.mean(avg_db), np.mean(inst_db)


def read_serial_port():
    return random.randint(0, 100)

def handle_client(conn, addr):
    print(f"Connecté à {addr}")
    while True:
        command = input("Entrez une commande: ")
        if command == "exit":
            break
        conn.sendall(command.encode())

    conn.close()

def auto_handle_client(conn, addr):
    print(f"Connecté à {addr}")
    while True:
        avg_mean, inst_mean = update_db()
        cmd = ""
        duration = random.randint(20, 40)
        if inst_mean - avg_mean > storm_trigger:
            print("Storm is trigerred !!")
            print("thunder " + str(duration))
            cmd = "thunder " + str(duration)
            time.sleep(duration)
        else :
            print(random.choice(anims) + str(duration))
            cmd = random.choice(anims) + str(duration)
        conn.sendall(cmd.encode())
        time.sleep(1)
    conn.close()

def nomic_auto_handle_client(conn, addr):
    print(f"Connecté à {addr}")
    while True:
        duration = random.randint(20, 40)
        cmd = random.choice(auto_anims) + str(duration)
        print("Commande envoyée : " + cmd)
        conn.sendall(cmd.encode())
        time.sleep(5)

    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    clients = []

    if not AMA0:
        while True:
            print("No microphone detected - Random mode")
            conn, addr = s.accept()
            #client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread = threading.Thread(target=nomic_auto_handle_client, args=(conn, addr))
            client_thread.start()
    else:
        print("Micro detected")
        fill_values(wait)
        print("Microphone calibration done")
        while True:
            conn, addr = s.accept()
            #client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread = threading.Thread(target=auto_handle_client, args=(conn, addr))
            client_thread.start()