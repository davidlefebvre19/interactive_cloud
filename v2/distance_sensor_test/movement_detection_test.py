import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

Trig = 16
Echo = 18

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

GPIO.output(Trig, False)


# Calibration before detecting movement
# We wait until the sensor is immobile and in range

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


def sensing_movement(passages):
    previous_dist = None
    passage = 0
    print("Movement detection test start")
    while passage < passages:
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
            if abs(int(previous_dist - distance)) >= 15:
                print("movement detected ! movements counter : ", passage)
                passage += 1
            previous_dist = distance

    print("Test done !")


if __name__ == "__main__":
    calibration()
    passages = input("nombre de passages requis :")
    sensing_movement(passages)