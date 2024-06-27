import time
import random
from rpi_ws281x import *

# Configuration des LED
PIN = 12
NUM_LEDS = 17
BRIGHTNESS = 100
FADE_OUT_RATE = 5

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

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

try:
    while True:
        rain_drop(strip)
        update_leds(strip)
        time.sleep(0.1)

except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()