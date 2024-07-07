import time
import random
from rpi_ws281x import *

# Configuration des LED
PIN = 12
NUM_LEDS = 300
BRIGHTNESS = 255
DELAY = 0.05  # 10ms
ZONE_LENGTH = 5  # Longueur de chaque zone
FADE_OUT_RATE = 10  # Vitesse du fondu
LIGHTNING_COLOR = Color(255, 255, 0)

# Création de l'objet strip pour contrôler les LED
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

# Définition des couleurs
red = Color(255, 0, 0)
yellow = Color(255, 255, 0)
blue = Color(0, 0, 255)
colors = [red, yellow, blue]
currentColorIndex = 0


def colorWipe(strip, color, wait_ms=10):
    """ Wipe color across display a pixel at a time. """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms)

def lightning_effect(strip, zone, fade_out_rate):
    """ Créer un effet d'éclair dans une zone spécifique """
    start_led = random.randint(zone * ZONE_LENGTH, (zone + 1) * ZONE_LENGTH - 1)
    end_led = random.randint(start_led, (zone + 1) * ZONE_LENGTH - 1)

    # Premier clignotement
    for i in range(start_led, end_led):
        strip.setPixelColor(i, LIGHTNING_COLOR)
    strip.show()
    time.sleep(0.05)  # Durée du clignotement

    # Éteindre les LEDs
    for i in range(start_led, end_led):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

    # Deuxième clignotement avec fondu
    for i in range(start_led, end_led):
        strip.setPixelColor(i, LIGHTNING_COLOR)
    strip.show()
    time.sleep(0.05)  # Durée du clignotement

    # Fondu
    for brightness in range(255, 0, -fade_out_rate):
        for i in range(start_led, end_led):
            strip.setPixelColor(i, Color(brightness, brightness, 0))
        strip.show()
        time.sleep(0.01)
def wheel(pos):
    """ Generate rainbow colors across 0-255 positions. """
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)



try:
    while True:
        # Update the animation
        colorWipe(strip, colors[currentColorIndex], DELAY)
        currentColorIndex = (currentColorIndex + 1) % len(colors)

except KeyboardInterrupt:
    colorWipe(strip, Color(0, 0, 0), 10)
