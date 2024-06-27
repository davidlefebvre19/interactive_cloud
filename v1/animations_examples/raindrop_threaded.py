from rpi_ws281x import *
import time
import random
import threading

# Configuration des LED
FADE_OUT_RATE = 5
NUM_LEDS = 17



# Couleur de la pluie (bleu)
RAIN_COLOR = Color(0, 0, 255)

# Tableaux pour suivre l'état de chaque LED
led_brightness = [0 for _ in range(NUM_LEDS)]
is_raining = [False for _ in range(NUM_LEDS)]

def update_leds(strip):
    """ Mettre à jour l'état de la bande LED """
    for i in range(NUM_LEDS):
        if led_brightness[i] > 0:
            led_brightness[i] = max(led_brightness[i] - FADE_OUT_RATE, 0)
            strip.setPixelColor(i, Color(0, 0, led_brightness[i]))
            if led_brightness[i] == 0:
                is_raining[i] = False
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def rain_drop(strip):
    """ Créer une goutte de pluie """
    start_led = random.randint(0, strip.numPixels() - 1)
    if not is_raining[start_led]:
        led_brightness[start_led] = 255  # Luminosité maximale pour commencer
        is_raining[start_led] = True

def run_rain_animation(stop_event, strip):
    while not stop_event.is_set():
        rain_drop(strip)
        update_leds(strip)
        time.sleep(0.1)

    # Éteindre toutes les LEDs à la fin
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()