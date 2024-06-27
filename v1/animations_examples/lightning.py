from rpi_ws281x import *
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 17
BRIGHTNESS = 255
DELAY = 0.05  # 10ms

# Création de l'objet strip pour contrôler les LED
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def colorWipe(strip, color, wait_ms=10):
    """ Wipe color across display a pixel at a time. """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms)
import time
import random
from rpi_ws281x import *

# Configuration des LED
PIN = 12
NUM_LEDS = 17
BRIGHTNESS = 255
ZONE_LENGTH = 5  # Longueur de chaque zone
FADE_OUT_RATE = 10  # Vitesse du fondu

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

# Couleur de l'éclair (jaune)
LIGHTNING_COLOR = Color(255, 255, 0)


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


try:
    while True:
        for zone in range(NUM_LEDS // ZONE_LENGTH):
            if random.choice([True, False]):  # 50% de chance d'activer l'éclair
                lightning_effect(strip, zone, FADE_OUT_RATE)
        time.sleep(random.uniform(0.1, 0.5))  # Intervalle aléatoire entre les éclairs

except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
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

# Définition des couleurs
red = Color(255, 0, 0)
yellow = Color(255, 255, 0)
blue = Color(0, 0, 255)
colors = [red, yellow, blue]
currentColorIndex = 0

try:
    while True:
        # Update the animation
        colorWipe(strip, colors[currentColorIndex], DELAY)
        currentColorIndex = (currentColorIndex + 1) % len(colors)

except KeyboardInterrupt:
    colorWipe(strip, Color(0, 0, 0), 10)
