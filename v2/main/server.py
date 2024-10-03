import socket
import threading
import time
import RPi.GPIO as GPIO
import random

#server constant variables
host = '127.0.0.1'
port = 65432

#anims variables
anims = ["c", "r"]

# dist sensor init
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

Trig = 16
Echo = 18

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

GPIO.output(Trig, False)

def calibration():
    stable_count = 0
    previous_dist = None

    print("calibration start")
    while stable_count < 10:
        time.sleep(1)

        GPIO.output(Trig, True)
        time.sleep(0.00001)
        GPIO.output(Trig, False)

        while GPIO.input(Echo) == 0:  # Emission de l'ultrason
            debutImpulsion = time.time()

        while GPIO.input(Echo) == 1:  # Retour de l'Echo
            finImpulsion = time.time()

        distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  # Vitesse du son = 340 m/s
        print("current distance : ", distance)
        if previous_dist == None:
            previous_dist = distance
            pass
        else:
            if abs(int(previous_dist - distance)) <= 15:
                stable_count += 1
            previous_dist = distance

    print("calibration done !")
    return previous_dist

def sensing_and_sending(max_dist, conn, addr):
    previous_dist = None
    passage = 0
    print("Movement detection test start")
    # Another mecanism than while true may be needed here
    while True:
        time.sleep(1)

        cmd = ""

        GPIO.output(Trig, True)
        time.sleep(0.1)
        GPIO.output(Trig, False)

        while GPIO.input(Echo) == 0:  # Emission de l'ultrason
            debutImpulsion = time.time()

        while GPIO.input(Echo) == 1:  # Retour de l'Echo
            finImpulsion = time.time()

        distance = round((finImpulsion - debutImpulsion) * 340 * 100 / 2, 1)  # Vitesse du son = 340 m/s
        print("current distance : ", distance)
        if previous_dist == None:
            previous_dist = distance
            pass
        else:
            duration = random.randint(15, 25)
            if abs(int(previous_dist - distance)) >= 15 and distance <= max_dist:
                # Movement detected !
                print("movement detected -> triggering thunder mecanism !")
                cmd = "t " + str(duration)
                print(cmd)
            else:
                # Chill ...
                print("no movement detected... calm / rain mecanism")
                cmd = random.choice(anims) + " " + str(duration)
            conn.sendall(cmd.encode())
            previous_dist = distance

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    clients = []

    # Try Except needed for calibration !!
    max_dist = calibration()
    if max_dist != None:
        #While true may be needed here
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=sensing_and_sending, args=(max_dist, conn, addr))
            client_thread.start()

