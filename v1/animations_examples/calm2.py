from rpi_ws281x import *
import time
import random

# Configuration des LED
PIN = 12
NUM_LEDS = 17
BRIGHTNESS = 255
HALO_SIZE = 3  # Taille de chaque halo
FADE_RATE = 5  # Vitesse du fondu
DELAY = 0.05   # Délai entre chaque mise à jour d'animation

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def create_halo(strip, start_led, halo_size, max_brightness=255, fade_rate=FADE_RATE):
    """ Créer un halo qui s'allume et s'éteint. """
    # Fade in
    for brightness in range(0, max_brightness, fade_rate):
        for i in range(start_led, min(start_led + halo_size, strip.numPixels())):
            strip.setPixelColor(i, Color(brightness, brightness, brightness))
        strip.show()
        time.sleep(0.01)

    time.sleep(DELAY)

    # Fade out
    for brightness in range(max_brightness, 0, -fade_rate):
        for i in range(start_led, min(start_led + halo_size, strip.numPixels())):
            strip.setPixelColor(i, Color(brightness, brightness, brightness))
        strip.show()
        time.sleep(0.01)

try:
    current_led = 0
    while True:
        create_halo(strip, current_led, HALO_SIZE)
        current_led = (current_led + 1) % NUM_LEDS

except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
